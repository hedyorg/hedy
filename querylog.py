import time
import collections
import functools
import threading
import logging
import os
import datetime
import resource
import traceback
import logging

logger = logging.getLogger('querylog')

class LogRecord:
    """A log record."""
    def __init__(self, **kwargs):
        self.start_time = time.time()
        self.start_rusage = resource.getrusage(resource.RUSAGE_SELF)
        self.attributes = kwargs
        self.set(
            start_time=dtfmt(self.start_time),
            fault=0)

        dyno = os.getenv('DYNO')
        if dyno:
            self.set(dyno=dyno)

    def finish(self):
        end_time = time.time()
        end_rusage = resource.getrusage(resource.RUSAGE_SELF)
        self.set(
            end_time=dtfmt(end_time),
            user_ms=ms_from_fsec(end_rusage.ru_utime - self.start_rusage.ru_utime),
            sys_ms=ms_from_fsec(end_rusage.ru_stime - self.start_rusage.ru_stime),
            duration_ms=ms_from_fsec(end_time - self.start_time))

        LOG_QUEUE.add(self)

    def set(self, **kwargs):
        self.attributes.update(kwargs)

    def update(self, dict):
        self.attributes.update(dict)

    def timer(self, name):
        return LogTimer(self, name)

    def inc(self, name, amount=1):
        if name in self.attributes:
            self.attributes[name] = self.attributes[name] + amount
        else:
            self.attributes[name] = amount

    def inc_timer(self, name, time_ms):
        self.inc(name + '_ms', time_ms)
        self.inc(name + '_cnt')

    def record_exception(self, exc):
        self.set(fault=1, error_message=str(exc))

    def as_data(self):
        return self.attributes

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if value:
            self.record_exception(value)
        self.finish()


class NullRecord(LogRecord):
    """A dummy log record that doesn't do anything.

    Will be returned if we don't have a default record.
    """
    def __init__(self, **kwargs): pass
    def finish(self): pass
    def set(self, **kwargs): pass


THREAD_LOCAL = threading.local()
THREAD_LOCAL.current_log_record = NullRecord()

def begin_global_log_record(**kwargs):
    """Open a new global log record with the given attributes."""
    THREAD_LOCAL.current_log_record = LogRecord(**kwargs)


def finish_global_log_record(exc=None):
    """Finish the global log record."""
    record = THREAD_LOCAL.current_log_record
    if exc:
        record.record_exception(exc)
    record.finish()
    THREAD_LOCAL.current_log_record = NullRecord()


def log_value(**kwargs):
    """Log values into the currently globally active Log Record."""
    THREAD_LOCAL.current_log_record.set(**kwargs)


def log_time(name):
    """Log a time into the currently globally active Log Record."""
    return THREAD_LOCAL.current_log_record.timer(name)

def log_counter(name, count=1):
    """Increase the count of something in the currently globally active Log Record."""
    return THREAD_LOCAL.current_log_record.inc(name, count)


def timed(fn):
    """Function decorator to make the given function timed into the currently active log record."""
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        with log_time(fn.__name__):
            return fn(*args, **kwargs)

    return wrapped


def dtfmt(timestamp):
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    return dt.isoformat() + 'Z'


class LogTimer:
    """A quick and dirty timer."""
    def __init__(self, record, name):
        self.record = record
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, tb):
        delta = ms_from_fsec(time.time() - self.start)
        self.record.inc_timer(self.name, delta)


class LogQueue:
    """A queue of records that still need to be written out.

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
    def __init__(self, batch_window_s, do_print=False):
        self.records_queue = collections.defaultdict(list)
        self.batch_window_s = batch_window_s
        self.transmitter = None
        self.do_print = do_print
        self.mutex = threading.Lock()
        self.thread = threading.Thread(target=self._write_thread, name='QueryLogWriter', daemon=True)
        self.thread.start()

    def add(self, record):
        bucket = div_clip(time.time(), self.batch_window_s)
        data = record.as_data()

        if self.do_print:
            logging.debug(repr(data))

        with self.mutex:
            self.records_queue[bucket].append(data)

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


def ms_from_fsec(x):
    """Milliseconds from fractional seconds."""
    return int(x * 1000)



LOG_QUEUE = LogQueue(batch_window_s=300)
