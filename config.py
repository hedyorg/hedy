import os
import socket
from pathlib import Path

ROOT_DIR = Path(__file__).parent
CONTENT_DIR = ROOT_DIR / 'content'
GRAMMARS_DIR = ROOT_DIR / 'grammars'

app_name = os.getenv('HEROKU_APP_NAME', socket.gethostname())
dyno = os.getenv('DYNO')
athena_query = os.getenv('AWS_ATHENA_PREPARE_STATEMENT')

config = {
    'port': os.getenv('PORT') or 8080,
    'session': {
        'cookie_name': 'hedy',
        # in minutes
        'session_length': 60 * 24 * 14,
        'reset_length': 60 * 4,
        'invite_length': 60 * 24 * 7
    },
    'email': {
        'sender': 'Hedy <hello@hedy.org>',
        'region': 'eu-central-1',
    },
    # The bcrypt library's default is 12
    'bcrypt_rounds': 9,
    'dynamodb': {
        'region': 'eu-west-1'
    },
    's3-query-logs': {
        'bucket': 'hedy-query-logs',
        'prefix': app_name + '/',
        # Make logs from different instances/processes unique
        'postfix': ('-' + dyno if dyno else '') + '-' + str(os.getpid()),
        'region': 'eu-west-1'
    },
    's3-parse-logs': {
        'bucket': 'hedy-parse-logs',
        'prefix': app_name + '/',
        # Make logs from different instances/processes unique
        'postfix': ('-' + dyno if dyno else '') + '-' + str(os.getpid()),
        'region': 'eu-west-1'
    },
    's3-activity-logs': {
        'bucket': 'hedy-activity-logs',
        'prefix': app_name + '/',
        # Make logs from different instances/processes unique
        'postfix': ('-' + dyno if dyno else '') + '-' + str(os.getpid()),
        'region': 'eu-west-1'
    },
    'athena': {
        'region': 'eu-west-1',
        'database': 'hedy-logs',
        'prepare_statement': athena_query,
        's3_output': 's3://hedy-query-outputs/',
        'max_results': 50
    },
    # enables the quiz environment by setting the config variable on True
    'quiz-enabled': True,
}
