import logging
import os
from collections import namedtuple

import boto3
from retrying import retry

from config import config

logger = logging.getLogger(__name__)


def _get_value(filters, name, default):
    return f"'{filters.get(name, default) or default}'"


QueryResult = namedtuple("QueryResult", ["id", "status"])


class AwsAthenaClient:
    @staticmethod
    def from_env():
        if os.getenv("AWS_ACCESS_KEY_ID"):
            db = boto3.client("athena", region_name=config["athena"]["region"])
            database = config["athena"]["database"]
            s3_output = config["athena"]["s3_output"]
            return AwsAthenaClient(db, database, s3_output)
        logger.warning("Unable to initialize Athena client (missing AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY)")
        return None

    def __init__(self, client, database, s3_output):
        self.client = client
        self.database = database
        self.s3_output = s3_output

    @retry(stop_max_attempt_number=5, wait_exponential_multiplier=1000, wait_exponential_max=10 * 1000)
    def poll_query_status(self, query_execution_id):
        result = self.client.get_query_execution(QueryExecutionId=query_execution_id)
        state = result["QueryExecution"]["Status"]["State"]
        if state == "SUCCEEDED":
            return result
        if state == "FAILED":
            return result
        raise Exception

    def start_query(self, query):
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": self.database},
            ResultConfiguration={"OutputLocation": self.s3_output},
        )

        return response["QueryExecutionId"]

    def get_query_results(self, query_execution_id, next_token=None, max_results=50):
        params = {"QueryExecutionId": query_execution_id, "MaxResults": max_results}
        if next_token:
            params["NextToken"] = next_token

        return self.client.get_query_results(**params)


class LogFetcher:
    def __init__(self, client):
        self.client = client

    def query(self, filters):
        query = self._build_query(filters)
        query_exec_id = self.client.start_query(query)
        query_status = self.client.poll_query_status(query_exec_id)

        return QueryResult(query_exec_id, query_status["QueryExecution"]["Status"]["State"])

    def get_query_results(self, query_execution_id, next_token=None):
        max_results = config["athena"]["max_results"]
        data = self.client.get_query_results(query_execution_id, next_token, max_results)
        return self._result_to_response(data, next_token is None), data.get("NextToken")

    def _build_query(self, filters):
        # For now we use a pre-created Athena prepared statement, re-evaluate after feedback about the query options
        filters_with_values = {k: v for k, v in filters.items() if v is not None}

        start = _get_value(filters_with_values, "start", "2022-01-01")
        end = _get_value(filters_with_values, "end", "2099-12-31")
        exception = _get_value(filters_with_values, "exception", "%")
        level = _get_value(filters_with_values, "level", "%")
        username = _get_value(filters_with_values, "username", "%")

        prep_statement = config["athena"]["prepare_statement"]
        return f"EXECUTE {prep_statement} USING {start}, {end}, {exception}, {level}, {username};"

    def _result_to_response(self, data, is_first_batch):
        headers, rows = self._get_rows_and_headers(data)
        # is_first_batch is used to cut the first data row which contains csv headers
        if is_first_batch:
            rows = rows[1:]
        return [self._to_row_response(headers, r) for r in rows]

    def _get_rows_and_headers(self, data):
        try:
            data_rows = data["ResultSet"]["Rows"]
            rows = [r.get("Data") for r in data_rows if r.get("Data")]
            data_columns = data["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]
            headers = [c["Name"] for c in data_columns]
            return headers, rows
        except KeyError or TypeError:
            return [], []

    def _to_row_response(self, headers, data):
        row = [d.get("VarCharValue") for d in data]
        return (
            {}
            if len(row) != len(headers)
            else {headers[i]: self._format_if_date(headers[i], row[i]) for i in range(0, len(headers))}
        )

    def _format_if_date(self, header, value):
        return value.split(".")[0] if header == "date" else value


athena_client = AwsAthenaClient.from_env()
log_fetcher = LogFetcher(athena_client)
