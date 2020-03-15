import requests
import os
import sys
import json

def main():
    """Fetch and print the contents of the logging collection in jsonbin.io

    FIXME: This could/should be doing queries, but for now we just list everything.
    """
    key = os.getenv('JSONBIN_SECRET_KEY')
    collection = os.getenv('JSONBIN_COLLECTION_ID')

    if key is None or collection is None:
        raise RuntimeError('Set JSONBIN_SECRET_KEY and JSONBIN_COLLECTION_ID if you want to log (disabled for now)')

    progress = sys.stderr

    headers = {'secret-key': key}

    progress.write('Listing collection... (this may take a while)\n')
    list_response = requests.get(jb_url(f'/e/collection/{collection}/all-bins'), headers=headers)
    listing = json.loads(list_response.text)
    if not listing['success']:
        raise RuntimeError('Server error: ' + listing['message'])

    bins = []

    progress.write(f'{len(listing["records"])} bins found\n')

    for record in listing['records']:
        progress.write('.')
        progress.flush()
        bin = json.loads(requests.get(jb_url(f'/b/' + record['id']), headers=headers).text)
        bins.append(bin)
    progress.write('\n')
    progress.flush()

    # Sort by sessions and date
    bins.sort(key=lambda b: (b.get('session', ''), b.get('date', '')))

    # Print all
    for bin in bins:
        print(json.dumps(bin))


def jb_url(url):
    return 'https://api.jsonbin.io' + url


if __name__ == '__main__':
    main()