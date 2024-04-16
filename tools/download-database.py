# A script to download all Dynamo tables into an SQLite database
import argparse
import sqlite3
import decimal
import os
from os import path
import json
import re

import boto3
from boto3.dynamodb.types import TypeDeserializer
from tqdm import tqdm

DDB_DESERIALIZER = TypeDeserializer()


def main():

    REGION = 'eu-west-1'

    defs = TableDefinitions()
    defs.add('hedy-beta-achievements')
    defs.add('hedy-beta-adventures')
    defs.add('hedy-beta-classes')
    defs.add('hedy-beta-class_customizations')
    defs.add('hedy-beta-invitations')
    defs.add('hedy-beta-parsons')
    defs.add('hedy-beta-program-stats')
    defs.add('hedy-beta-programs')
    defs.add('hedy-beta-public_profiles')
    defs.add('hedy-beta-quiz-stats')
    defs.add('hedy-beta-quizAnswers')
    defs.add('hedy-beta-tokens')
    defs.add('hedy-beta-users')

    parser = argparse.ArgumentParser(description='Download DDB into SQLite')
    subparsers = parser.add_subparsers()
    cmd_download = subparsers.add_parser('download')
    cmd_download.set_defaults(command='download')

    cmd_insert = subparsers.add_parser('insert')
    cmd_insert.set_defaults(command='insert')

    args = parser.parse_args()
    if 'command' not in args or args.command == 'download':
        ddb = boto3.client('dynamodb', region_name=REGION)
        dl = TableDownload(ddb, 'download')
        dl.download_all(defs)
    if 'command' not in args or args.command == 'insert':
        inserter = TableInserter('db.sqlite3', 'download')
        inserter.insert_all(defs)


class TableInserter:
    def __init__(self, dbfile, jsondirectory):
        self.db = sqlite3.connect(dbfile)
        self.jsondirectory = jsondirectory

    def insert_all(self, defs: 'TableDefinitions'):
        for table_name in defs.table_names:
            self.insert_table(table_name)

    def insert_table(self, table_name):
        print(table_name)
        with open(path.join(self.jsondirectory, f'{table_name}.json'), 'r', encoding='utf-8') as f:
            table_data = json.load(f)
        if not table_data['rows']:
            return

        table_data['rows'] = restore_types(table_data['rows'])

        columns = determine_columns(table_data['rows'])

        scalar_columns = [col for col in columns if not col.type.is_collection]
        keycolumns = [find_col(scalar_columns, k) for k in table_data['key']]

        table = SqlTableDef(table_name, scalar_columns, keycolumns)

        cursor = self.db.cursor()
        cursor.execute(table.drop_statement)
        cursor.execute(table.create_statement)

        cursor.executemany(
            table.insert_statement,
            table.extract_table_values(table_data['rows']))

        # Lists
        for listcol in (col for col in columns if col.type.is_list or col.type.is_set):
            typ = SqlType.most_generic(value for row in table_data['rows']
                                       for value in row.get(listcol.original_name, []))
            onetomanycol = SqlColumn(listcol.original_name, typ)

            onetomanytable = SqlTableDef(
                f'{table.table_name}_{onetomanycol.name}',
                table.key_columns + [onetomanycol],
                table.key_columns + [onetomanycol] if listcol.type.is_set else [])
            print(onetomanytable.table_name)
            cursor.execute(onetomanytable.drop_statement)
            try:
                # The `classes` table contains a list of objects, which this script can't
                # deal with. Catch the error, but continue.
                cursor.execute(onetomanytable.create_statement)
            except Exception as e:
                print(f'Dropping column {listcol.name} (running \'{onetomanytable.create_statement}\' leads to {e})')
                continue

            one_to_many_data = []
            for row in table_data['rows']:
                for listvalue in row.get(listcol.original_name, []):
                    one_to_many_data.append(tuple(
                        [row.get(key_col.original_name) for key_col in table.key_columns]
                        +
                        [listvalue]))

            cursor.executemany(onetomanytable.insert_statement, one_to_many_data)

        # Maps (not implemented yet)
        for mapcol in (col for col in columns if col.type.is_map):
            print(f'Dropping column: {table.original_name}.{mapcol.original_name} (no support for map columns)')

        self.db.commit()


def find_col(cols, name):
    cs = [col for col in cols if col.original_name == name]
    if not cs:
        raise RuntimeError(f'Could not find col {name}')
    return cs[0]


class SqlColumn:
    def __init__(self, name, type: 'SqlType'):
        self.original_name = name
        self.name = slugify(name)
        self.type = type

        self.sql_def = f'"{self.name}" {self.type.sql_def}'

    def widen_type(self, type: 'SqlType'):
        self.type = self.type.unify(type)


class SqlTableDef:
    def __init__(self, table_name, columns, key_columns):
        self.original_name = table_name
        self.table_name = slugify(table_name)
        self.columns = columns
        self.key_columns = key_columns

    @property
    def drop_statement(self):
        return f'DROP TABLE IF EXISTS "{self.table_name}";'

    @property
    def create_statement(self):
        table_def = ', '.join(
            [col.sql_def for col in self.columns]
            +
            (['PRIMARY KEY(' + ', '.join(c.name for c in self.key_columns) + ')'] if self.key_columns else [])
        )

        return f'CREATE TABLE "{self.table_name}"({table_def});'

    @property
    def insert_statement(self):
        qmarks = ['?'] * len(self.columns)
        return f'INSERT INTO "{self.table_name}" VALUES({", ".join(qmarks)});'

    def extract_values(self, row):
        return tuple(row[c.original_name] if c.original_name in row else None for c in self.columns)

    def extract_table_values(self, table):
        return [self.extract_values(row) for row in table]


def determine_columns(rows):
    columns = {}
    for row in rows:
        for key, value in row.items():
            existing_col = columns.get(key)
            if existing_col:
                existing_col.widen_type(SqlType.of(value))
            else:
                columns[key] = SqlColumn(key, SqlType.of(value))
    return list(columns.values())


def make_col_def(name, typ):
    return f'"{name}" {typ}'


def slugify(x):
    return re.sub('[^a-zA-Z0-9]', '_', x)


class SqlType:
    @staticmethod
    def of(value):
        if isinstance(value, str):
            return SqlType('TEXT')
        if isinstance(value, int):
            return SqlType('INTEGER')
        if isinstance(value, float):
            return SqlType('REAL')
        if isinstance(value, set):
            return SqlType('+SET')
        if isinstance(value, list):
            return SqlType('+LIST')
        if isinstance(value, dict):
            return SqlType('+MAP')
        if value is None:
            return SqlType('NULL')
        raise RuntimeError(f'Do not know type of value {value}')

    @staticmethod
    def null():
        return SqlType('NULL')

    @staticmethod
    def most_generic(xs):
        t = SqlType.null()
        for x in xs:
            t = t.unify(SqlType.of(x))
        return t

    def __init__(self, type):
        self.type = type
        self.is_collection = type.startswith('+')
        self.is_set = type == '+SET'
        self.is_list = type == '+LIST'
        self.is_map = type == '+MAP'
        self.sql_def = type

    def unify(self, rhs):
        if self.type == rhs.type:
            return self
        if self.type == 'NULL':
            return rhs
        if rhs.type == 'NULL':
            return self

        types = [self.type, rhs.type]
        types.sort()

        if types == ['INTEGER', 'REAL']:
            return SqlType('REAL')
        if types == ['INTEGER', 'TEXT'] or types == ['REAL', 'TEXT']:
            return SqlType('TEXT')
        raise RuntimeError(f'Cannot unify types {self.type} and {rhs.type}')


class TableDefinitions:
    def __init__(self):
        self.table_names = []

    def add(self, table_name):
        self.table_names.append(table_name)


class TableDownload:
    def __init__(self, ddb, directory):
        self.ddb = ddb
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def download_all(self, defs):
        for table_name in defs.table_names:
            self.download_table(table_name)

    def download_table(self, table_name):
        print(table_name)
        description = self.ddb.describe_table(TableName=table_name)

        partition_key = [k['AttributeName'] for k in description['Table']['KeySchema'] if k['KeyType'] == 'HASH']
        sort_key = [k['AttributeName'] for k in description['Table']['KeySchema'] if k['KeyType'] == 'RANGE']

        key = [partition_key[0]] + ([sort_key[0]] if sort_key else [])

        columns = {a['AttributeName']: a['AttributeType'] for a in description['Table']['AttributeDefinitions']}

        rows = []
        with tqdm(total=description['Table']['ItemCount']) as progressbar:
            for page in self.ddb.get_paginator('scan').paginate(TableName=table_name):
                for row in page['Items']:
                    rows.append({key: DDB_DESERIALIZER.deserialize(value) for key, value in row.items()})
                    progressbar.update(1)

        with open(path.join(self.directory, f'{table_name}.json'), 'w', encoding='utf-8') as f:
            json.dump(dict(key=key, rows=rows, columns=columns), f, cls=DDBTypesEncoder)


class DDBTypesEncoder(json.JSONEncoder):
    """Encode some types to JSON that can occur in DynamoDB that are not natively serializable to JSON."""

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if int(o) == o:
                return int(o)
            return float(o)
        if isinstance(o, set):
            return {'@type': 'set', 'set': list(o)}
        return super(DDBTypesEncoder, self).default(o)


def restore_types(rows):
    """Decode all values that were encoded using DDBTypesEncoder."""
    def decode(o):
        if isinstance(o, dict) and o.get('@type') == 'set':
            return set(o['set'])
        return o
    return [{key: decode(value) for key, value in row.items()} for row in rows]


if __name__ == '__main__':
    main()
