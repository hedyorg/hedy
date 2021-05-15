"""Routines for interacting with AWS."""
import boto3
import os
import json
import logging
import config
import utils

def s3_transmitter_from_env():
    """Return an S3 transmitter, or return None."""
    have_aws_creds = os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY')

    if not have_aws_creds:
        logging.warning('Unable to initialize S3 querylogger (missing AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY)')
        return None

    return transmit_to_s3


def transmit_to_s3(timestamp, records):
    """Transmit logfiles to S3 with default config."""
    s3config = config.config['s3-query-logs']

    # No need to configure credentials, we've already confirmed they are in the environment.
    s3 = boto3.client('s3', region_name=s3config['region'])

    # Grouping in the key is important, we need this to zoom into an interesting
    # log period.
    key = s3config['prefix'] + utils.isoformat(timestamp) + s3config['postfix'] + '.jsonl'

    # Store as json-lines format
    body = '\n'.join(json.dumps(r) for r in records)

    s3.put_object(
        Bucket=s3config['bucket'],
        Key=key,
        StorageClass='STANDARD_IA', # Cheaper, applicable for logs
        Body=body)
    logging.debug(f'Wrote {len(records)} query logs to s3://{s3config["bucket"]}/{key}')