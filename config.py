import os
import socket

app_name = os.getenv('HEROKU_APP_NAME', socket.gethostname())
dyno = os.getenv('DYNO')

config = {
    'port': 5000,
    'session': {
        'cookie_name': 'hedy',
        # in minutes
        'session_length': 60 * 24 * 14
    },
    'email': {
        'sender': 'Hedy <hedy@felienne.com>',
        'region': 'eu-central-1',
    },
    'dynamodb': {
        'region': 'eu-central-1'
    },
    's3-query-logs': {
        'bucket': 'hedy-query-logs',
        'prefix': app_name + '/',
        # Make logs from different instances unique
        'postfix': '.' + dyno if dyno else '',
        'region': 'eu-central-1'
    },
}
