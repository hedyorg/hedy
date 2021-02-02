config = {
    'port': 5000,
    'session': {
        'cookie_name': 'hedy',
        # in minutes
        'session_length': 60 * 24
    },
    'email': {
        'sender': 'Hedy <hedy@felienne.com>',
        'region': 'eu-central-1',
    },
    'dynamodb': {
        'region': 'eu-central-1'
    }
}
