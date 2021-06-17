import os
import socket

app_name = os.getenv('HEROKU_APP_NAME', socket.gethostname())
dyno = os.getenv('DYNO')

config = {
    'port': os.getenv ('PORT') or 5000,
    'session': {
        'cookie_name': 'hedy',
        # in minutes
        'session_length': 60 * 24 * 14
    },
    'email': {
        'sender': 'Hedy <hedy@felienne.com>',
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
}
