import threading
import os
import json
import queue
import requests
import logging

logger = logging.getLogger('jsonbin')

class JsonBinLogger:
    """Logger for jsonbin.io

    Because writing records to jsonbin is rather slow, and since this is
    logging (where it's okay to do this on a best-effort basis), we
    push the logging to a separate thread.
    """

    @staticmethod
    def from_env_vars():
        """Create a new JsonBinLogger using standard environment variables."""
        key = os.getenv('JSONBIN_SECRET_KEY')
        collection = os.getenv('JSONBIN_COLLECTION_ID')

        if key is None or collection is None:
            logger.warn('Set JSONBIN_SECRET_KEY and JSONBIN_COLLECTION_ID if you want to log (disabled for now)')
            return NullJsonbinLogger()
        return JsonBinLogger(key, collection)

    def __init__(self, secret_key, collection_id):
        self.secret_key = secret_key
        self.collection_id = collection_id
        self.queue = queue.Queue()

        self.thread = threading.Thread(target=self._run, daemon=True, name='jsonbin_logger')
        self.thread.start()

    def log(self, obj):
        """Log a single object to the given jsonbin collection."""
        self.queue.put(obj)

        # Let's start off by printing warnings. If this turns out to be an
        # issue in the future, we might start dropping work.
        if self.queue.qsize() > 20:
            logger.warn(f'jsonbin logging queue is backing up, contains {self.queue.qsize()} items')

    def _run(self):
        logger.debug('jsonbin logger started')
        while True:
            obj = self.queue.get()

            try:
                response = requests.post('https://api.jsonbin.io/b', json=obj, headers={
                    'Content-Type': 'application/json',
                    'secret-key': self.secret_key,
                    'collection-id': self.collection_id,
                })

                # Try to read the response as JSON
                try:
                    resp = json.loads(response.text)

                    if resp['success']:
                        logger.info('Posted to jsonbin')
                    else:
                        logger.warning('Posting to jsonbin failed: ' + resp['message'])
                except Exception as e:
                    # Not JSON or no success field
                    logger.warning(f'Posting to jsonbin failed: {response.text}')
            except Exception as e:
                logger.exception(f'Error posting to jsonbin.')

class NullJsonbinLogger():
    """A jsonbin logger that doesn't actually do anything."""
    def log(self, obj):
        pass