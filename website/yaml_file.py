import os
import pickle

from ruamel import yaml

from utils import atomic_write_file, is_heroku

yaml_loader = yaml.YAML(typ="safe", pure=True)

YAML_FILES_CACHE = {}


class YamlFile:
    """Data from a YAML file, accessible as if it is a dictionary.

    Use like so:

        file = YamlFile.for_file('path/to/file.yaml')

        if file.exists():
            print(file['key1'])
        else:
            print('oh no')

    Since loading the YAML files tends to be slow:

    - Caches the loaded data in memory.
    - Can write a pickle file from the loaded data, so that the
      initial load may be slow but future loads from disk (after
      program restarts) will be faster (loading pickled data is ~400x
      faster than loading YAML directly).
    - Automatically invalidates all caching if the timestamp of the
      YAML file on disk changes.
    """

    @staticmethod
    def for_file(filename):
        """Factory function: return a singleton YamlFile instance for the given file."""
        if filename not in YAML_FILES_CACHE:
            YAML_FILES_CACHE[filename] = YamlFile(filename)
        return YAML_FILES_CACHE[filename]

    def __init__(self, filename, try_pickle=None):
        """Create a new YamlFile for the given filename.

        try_pickle controls on whether we pickle or not. Can be
        `True`, `False` or `None` -- in case of `None` pickling is
        determined automatically based on whether or not we appear
        to be running on Heroku. We don't pickle on dev workstations
        because it creates a mess of files.
        """
        self.filename = filename
        self.pickle_filename = f"{self.filename}.pickle"
        self.data = None
        self.timestamp = 0
        self.try_pickle = try_pickle

    def exists(self):
        return os.path.exists(self.filename)

    def to_dict(self):
        """Return the contents of the file as a plain dict, or an empty dict if the file doesn't exist.

        You should generally not need to use this: this object can be used in places
        where dicts are expected (except if the file doesn't exist, then accessing it will throw; we
        can consider changing that behavior to always return an empty dict).
        """
        if self.exists():
            return self.access()
        return {}

    def access(self):
        """Access the data from memory.

        Load it if we haven't loaded it yet or the data on disk changed.
        """
        stat = os.stat(self.filename)
        if self.data is None or stat.st_mtime > self.timestamp:
            self.data = self.load(stat.st_mtime)
            self.timestamp = stat.st_mtime

        if not isinstance(self.data, dict):
            raise RuntimeError(f"Contents of {self.filename} needs to be a dict, got: {self.data}")

        return self.data

    def load(self, yaml_timestamp):
        """Load the data from disk.

        Load from a pickle file if available, or load the original YAML
        and write a pickle file otherwise.
        """
        try_pickle = self.try_pickle if self.try_pickle is not None else is_heroku()

        if not try_pickle:
            return self.load_uncached()

        stat = os.stat(self.pickle_filename) if os.path.exists(self.pickle_filename) else None
        if stat and stat.st_mtime >= yaml_timestamp:
            # Pickle file is newer than the YAML, just read that
            return self.load_pickle()

        data = self.load_uncached()

        # Write a pickle file, first write to a tempfile then rename
        # into place because multiple processes might try to do this in parallel,
        # plus we only want `path.exists(pickle_file)` to return True once the
        # file is actually complete and readable.
        with atomic_write_file(self.pickle_filename) as f:
            pickle.dump(data, f)

        return data

    def load_pickle(self):
        with open(self.pickle_filename, "rb") as f:
            return pickle.load(f)

    def load_uncached(self):
        """Load the source YAML file."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return yaml_loader.load(f)
        except IOError:
            return {}

    # Make this object look like a readonly 'dict'
    def __getitem__(self, key):
        return self.access()[key]

    def get(self, key, default=None):
        return self.access().get(key, default)

    def has_key(self, k):
        return k in self.access()

    def keys(self):
        return self.access().keys()

    def values(self):
        return self.access().values()

    def items(self):
        return self.access().items()

    def __contains__(self, item):
        return item in self.access()

    def __iter__(self):
        return iter(self.access())

    def __len__(self):
        return len(self.access())
