import time
import collections
import threading
import logging
import traceback
import logging

class LogQueue:
    """A queue of records that need to be written out to a web resource.

    For efficiency's sake, records are grouped into time windows of
    'batch_window_s' seconds (say, 5 minutes). x'es below indicate
    log record events:

          300               600               900
         |   x    x x      |             x   |
       --+-----------------+-----------------+---------
          ^                 ^                 ^
        wake               wake              wake

    Upon 'wake' events (every batch window seconds), a background thread
    wakes up and collects all events from previous time windows.

    We need to use a mutex since the dict we keep the queue in is not
    thread-safe. We do as little work as possible every time we hold the mutex
    to allow for maximum parallelism.
    """
    def __init__(self, name, batch_window_s, do_print=False):
        self.records_queue = collections.defaultdict(list)
        self.batch_window_s = batch_window_s
        self.transmitter = None
        self.do_print = do_print
        self.mutex = threading.Lock()
        self.name = name
        self.thread = threading.Thread(target=self._write_thread, name=f'{name}Writer', daemon=True)
        self.thread.start()

    def add(self, record):
        bucket = div_clip(time.time(), self.batch_window_s)

        if self.do_print:
            logging.debug(repr(record))

        with self.mutex:
            self.records_queue[bucket].append(record)

    def set_transmitter(self, transmitter):
        """Configure a function that will be called for every set of records.

        The function looks like:

            def transmitter(timestamp, records) -> Boolean:
                ...
        """
        self.transmitter = transmitter

    def _save_records(self, timestamp, records):
        if self.transmitter:
            return self.transmitter(timestamp, records)
        else:
            count = len(records)
            logging.warn(f'No querylog transmitter configured, {count} records dropped')

    def _write_thread(self):
        """Background thread which will wake up every batch_window_s seconds to emit records from the queue."""
        next_wake = div_clip(time.time(), self.batch_window_s) + self.batch_window_s
        while True:
            try:
                # Wait for next wake time
                time.sleep(max(0, next_wake - time.time()))

                # Once woken, see what buckets we have left to push (all buckets
                # with numbers lower than next_wake)
                with self.mutex:
                    keys = list(self.records_queue.keys())
                keys.sort()
                buckets_to_send = [k for k in keys if k < next_wake]

                for bucket_ts in buckets_to_send:
                    # Get the records out of the queue
                    with self.mutex:
                        bucket_records = self.records_queue[bucket_ts]

                    # Try to send the records
                    success = self._save_records(bucket_ts, bucket_records)

                    # Only remove them from the queue if sending didn't fail
                    if success != False:
                        with self.mutex:
                            del self.records_queue[bucket_ts]
            except Exception as e:
                traceback.print_exc(e)
            next_wake += self.batch_window_s


def div_clip(x, y):
    """Return the highest value < x that's a multiple of y."""
    return int(x // y) * y
