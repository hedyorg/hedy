import logging

from . import aws_helpers, log_queue

logger = logging.getLogger(__name__)


class NullLogger:
    """A logger that doesn't actually do anything."""

    def log(self, obj):
        pass


class S3ParseLogger:
    """A logger that logs to S3.
    """

    @staticmethod
    def from_env_vars():
        transmitter = aws_helpers.s3_parselog_transmitter_from_env()
        if not transmitter:
            return NullLogger()

        S3_LOG_QUEUE.set_transmitter(transmitter)
        return S3ParseLogger()

    def log(self, obj):
        S3_LOG_QUEUE.add(obj)


S3_LOG_QUEUE = log_queue.LogQueue("parse", batch_window_s=300)
S3_LOG_QUEUE.try_load_emergency_saves()


def emergency_shutdown():
    """The process is being killed. Do whatever needs to be done to save the logs."""
    S3_LOG_QUEUE.emergency_save_to_disk()
