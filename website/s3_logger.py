import logging
import json
import os

from . import aws_helpers, log_queue

logger = logging.getLogger(__name__)


should_log_activity = os.getenv("LOG_USER_ACTIVITY")


class NullLogger:
    """A logger that doesn't actually do anything."""

    def __init__(self, file_path="activity_data.json", **kwargs):
        self.is_tracking = kwargs.get("tracking")
        self.file_path = file_path

    def open_file(self):
        """Opens the json file and returns its data."""
        if self.is_tracking:
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except IOError as e:
                print(f"Error reading JSON file: {e}")
                return []

    def log(self, obj):
        """Logs an event with its type and data to the CSV file."""
        print("shoudl log?? \n\n", should_log_activity)
        if self.is_tracking and should_log_activity:
            data = self.open_file()
            data.extend(obj)
            try:
                with open(self.file_path, 'w') as f:
                    json.dump(data, f, indent=4)
            except IOError as e:
                print(f"Error logging to JSON file: {e}")


class S3Logger:
    """A logger that logs to S3.
    """

    def __init__(self, name: str, **kwargs) -> None:
        self.s3_log_queue = log_queue.LogQueue(name, batch_window_s=300)
        self.s3_log_queue.try_load_emergency_saves()

        if kwargs.get("tracking"):
            transmitter = aws_helpers.s3_parselog_transmitter_from_env(config_key="s3-activity-logs")
        else:
            transmitter = aws_helpers.s3_parselog_transmitter_from_env()

        self.transmitter = transmitter

        if transmitter:
            self.s3_log_queue.set_transmitter(transmitter)
        else:
            self.null_logger = NullLogger(**kwargs)

    def log(self, obj):
        if not self.transmitter:
            return self.null_logger.log(obj)
        self.s3_log_queue.add(obj)

    def emergency_shutdown(self):
        """The process is being killed. Do whatever needs to be done to save the logs."""
        self.s3_log_queue.emergency_save_to_disk()
