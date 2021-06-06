import time
import functools
import threading
import logging
import os
import datetime
import resource
import logging

from . import log_queue

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

        LOG_QUEUE.add(self.as_data())

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


def ms_from_fsec(x):
    """Milliseconds from fractional seconds."""
    return int(x * 1000)


LOG_QUEUE = log_queue.LogQueue('querylog', batch_window_s=300)
