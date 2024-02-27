import logging
import json

from . import aws_helpers, log_queue

logger = logging.getLogger(__name__)


class FileLogger:
    """A logger that logs obj to a given file_logger.json file."""

    def __init__(self):
        self.file_path = "file_logger.json"

    def open_file(self):
        """Opens the json file and returns its data."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except IOError as e:
            print(f"Error reading JSON file: {e}")
            return []

    def log(self, obj):
        """Logs an event with its type and data to the CSV file."""
        data = self.open_file()
        data.extend(obj)
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error logging to JSON file: {e}")


class NullLogger:
    """A logger that doesn't actually do anything."""

    def log(self, obj):
        pass


class S3Logger:
    """A logger that logs to S3, to a file, or nothing.

    - write_to_file(bool, optional):**
        - Defaults to `False`.
        - If `True`, logs will be additionally written to a local file named file_logger.json.

    **Note:**

    - If `write_to_file` is `False`, a NullLogger (which doesn't log anything) will be used.
    """

    def __init__(self, name: str, config_key: str, write_to_file: bool = False, **kwargs) -> None:
        self.s3_log_queue = log_queue.LogQueue(name, batch_window_s=300)
        self.s3_log_queue.try_load_emergency_saves()

        transmitter = aws_helpers.s3_parselog_transmitter_from_env(config_key=config_key)

        if transmitter:
            self.s3_log_queue.set_transmitter(transmitter)
        else:
            self.local_logger = FileLogger() if write_to_file else NullLogger()

        self.transmitter = transmitter

    def log(self, obj):
        if not self.transmitter:
            self.local_logger.log(obj)
        else:
            self.s3_log_queue.add(obj)

    def emergency_shutdown(self):
        """The process is being killed. Do whatever needs to be done to save the logs."""
        self.s3_log_queue.emergency_save_to_disk()
