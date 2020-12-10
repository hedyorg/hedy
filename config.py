config = {
    'port': 5000,
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db':   0
    },
    'session': {
        'cookie_name': 'hedy',
        # in minutes
        'session_length': 60 * 24
    },
    'email': {
        'sender': 'Hedy <hedy@felienne.com>',
        'region': 'eu-central-1',
    }
}
