import threading
import os
import json
import queue
import requests
import logging

from . import log_queue
from . import aws_helpers

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
                response = requests.post('https://api.jsonbin.io/v3/b', json=obj, headers={
                    'Content-Type': 'application/json',
                    'X-Master-Key': self.secret_key,
                    'X-Collection-Id': self.collection_id,
                })

                # Try to read the response as JSON
                try:
                    resp = json.loads(response.text)

                    if response.status_code == 200:
                        logger.info('Posted to jsonbin')
                    else:
                        logger.warning(f'Posting to jsonbin failed: {response.status_code} {resp["message"]}')
                except Exception:
                    # Not JSON or no success field
                    logger.exception(f'Posting to jsonbin failed: {response.text}')
            except Exception:
                logger.exception(f'Error posting to jsonbin.')


class NullJsonbinLogger():
    """A jsonbin logger that doesn't actually do anything."""
    def log(self, obj):
        pass


class MultiParseLogger():
    """A logger that forwards to other loggers."""
    def __init__(self, *loggers):
        self.loggers = loggers

    def log(self, obj):
        for logger in self.loggers:
            logger.log(obj)


class S3ParseLogger():
    """A logger that logs to S3.

    - Well then why is it in a file called 'jsonbin.py'?

    - Legacy, young grasshopper. Legacy.
    """
    @staticmethod
    def from_env_vars():
        transmitter = aws_helpers.s3_parselog_transmitter_from_env()
        if not transmitter:
            return NullJsonbinLogger()

        S3_LOG_QUEUE.set_transmitter(transmitter)
        return S3ParseLogger()

    def log(self, obj):
        S3_LOG_QUEUE.add(obj)


S3_LOG_QUEUE = log_queue.LogQueue('parse', batch_window_s=300)
S3_LOG_QUEUE.try_load_emergency_saves()

def emergency_shutdown():
    """The process is being killed. Do whatever needs to be done to save the logs."""
    S3_LOG_QUEUE.emergency_save_to_disk()