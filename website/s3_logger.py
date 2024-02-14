import logging
import csv

from . import aws_helpers, log_queue

logger = logging.getLogger(__name__)


class NullLogger:
    """A logger that doesn't actually do anything."""

    def __init__(self, file_path="tracking_data.csv", header=[], **kwargs):
        self.is_tracking = kwargs.get("tracking")
        self.file_path = file_path
        self.file_header = header
        self.open_file()

    def open_file(self):
        """Opens the CSV file in append mode, creating it if it doesn't exist."""
        if self.is_tracking:
            try:
                with open(self.file_path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    # Write header only if file is empty
                    if f.tell() == 0:
                        writer.writerow(self.file_header)
            except IOError as e:
                print(f"Error opening CSV file: {e}")

    def log(self, data):
        """Logs an event with its type and data to the CSV file."""
        if self.is_tracking:
            try:
                with open(self.file_path, 'a') as f:
                    writer = csv.writer(f)
                    # data should be a list of lists whose values correspond with the headers we set in self.open_file
                    writer.writerows(data)
            except IOError as e:
                print(f"Error logging to CSV file: {e}")


class S3ParseLogger:
    """A logger that logs to S3.
    """

    @staticmethod
    def from_env_vars(**kwargs):
        if kwargs.get("tracking"):
            transmitter = aws_helpers.s3_parselog_transmitter_from_env(config_key="s3-parse-tracking-logs")
        else:
            transmitter = aws_helpers.s3_parselog_transmitter_from_env()

        if not transmitter:
            return NullLogger(**kwargs)

        S3_LOG_QUEUE.set_transmitter(transmitter)
        return S3ParseLogger()

    def log(self, obj):
        S3_LOG_QUEUE.add(obj)


S3_LOG_QUEUE = log_queue.LogQueue("parse", batch_window_s=300)
S3_LOG_QUEUE.try_load_emergency_saves()


def emergency_shutdown():
    """The process is being killed. Do whatever needs to be done to save the logs."""
    S3_LOG_QUEUE.emergency_save_to_disk()
