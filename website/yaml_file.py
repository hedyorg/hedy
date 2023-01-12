import hashlib
import logging
from os import path
import os
import pickle
import re
import tempfile
from . import querylog

from ruamel import yaml

from utils import atomic_write_file
from flask import has_request_context, g

yaml_loader = yaml.YAML(typ="safe", pure=True)
logger = logging.getLogger(__name__)

YAML_FILES_CACHE = {}


class YamlFile:
    """Data from a YAML file, accessible as if it is a dictionary.

    Use like so:

        file = YamlFile.for_file('path/to/file.yaml')

        if file.exists():
            print(file['key1'])
        else:
            print('oh no')

    Since loading the YAML files tends to be slow (takes 1s to load all YAML
    files for a single language in the course of rendering the main code editor page),
    we do some caching work:

    - Caches the loaded data in memory, on the Flask 'current request globals' object.
      This means that accessing the same file twice in the same request will only load
      it once. If we don't do this, loading YAMLs takes 2s instead of 1 because of the
      duplicate loads.
      - To keep the application memory footprint low, we don't cache the data
        permanently, but drop it after the request is done.
    - After we have successfully loaded a YAML file, we write a pickled version
      of that YAML file to disk, so that we can load the pickled version faster in
      the future future  (loading pickled data is ~400x faster than parsing a YAML
      file).
      - Pickled files are purely a server-side optimization. The files should not be checked
        in, and in fact by default this class will only generate them when running on Heroku.
      - Nevertheless, we do some time stamp checking to make sure to read the pickle
        file if its timestamp is older than the YAML file's timestamp.
    """

    @staticmethod
    def for_file(filename):
        """Factory function: return a singleton YamlFile instance for the given file."""
        filename = path.abspath(filename)
        if filename not in YAML_FILES_CACHE:
            YAML_FILES_CACHE[filename] = YamlFile(filename)
        return YAML_FILES_CACHE[filename]

    def __init__(self, filename):
        """Create a new YamlFile for the given filename.

        try_pickle controls on whether we pickle or not. Can be
        `True`, `False` or `None` -- in case of `None` pickling is
        determined automatically based on whether or not we appear
        to be running on Heroku. We don't pickle on dev workstations
        because it creates a mess of files.
        """
        self.filename = filename
        self.pickle_filename = path.join(tempfile.gettempdir(), 'hedy_pickles',
                                         f"{pathname_slug(self.filename)}.pickle")

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
        # Obtain or create a per-request cache dictionary (if we have a request), or an unattached
        # cache object that will disappear after this function returns if we don't have a request.
        yaml_cache = g.setdefault('yaml_cache', {}) if has_request_context() else {}
        cached = yaml_cache.get(self.filename)
        if cached is not None:
            return cached

        data = self.load()

        if not isinstance(data, dict):
            raise RuntimeError(f"Contents of {self.filename} needs to be a dict, got: {data}")

        yaml_cache[self.filename] = data
        return data

    def load(self):
        """Load the data from disk.

        Load from a pickle file if available, or load the original YAML
        and write a pickle file otherwise.
        """
        yaml_ts = self._file_timestamp(self.filename)
        pickle_ts = self._file_timestamp(self.pickle_filename)

        if pickle_ts and pickle_ts > yaml_ts:
            # Pickle file is newer than the YAML, just read that
            return self.load_pickle()

        # Otherwise load uncached and save (atomically, since multiple processes might
        # be trying to write the pickle file in parallel)
        data = self.load_uncached()
        try:
            os.makedirs(path.dirname(self.pickle_filename), exist_ok=True)
            with atomic_write_file(self.pickle_filename) as f:
                pickle.dump(data, f)
        except IOError as e:
            logger.warn('Error writing pickled YAML: %s', e)

        return data

    @querylog.timed_as('load_yaml_pickled')
    def load_pickle(self):
        with open(self.pickle_filename, "rb") as f:
            return pickle.load(f)

    @querylog.timed_as('load_yaml_uncached')
    def load_uncached(self):
        """Load the source YAML file."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return yaml_loader.load(f)
        except IOError:
            return {}

    def _file_timestamp(self, filename):
        try:
            return os.stat(filename).st_mtime
        except FileNotFoundError:
            return None

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


def pathname_slug(x):
    """Turn a path name into an identifier we can use as a file name.

    Take into account that it may contain characters we want to remove,
    that the full path may be too long to use as a file name, and that
    it needs to remain unique.
    """
    x = re.sub(r'[^a-zA-Z0-9_-]', '', x)
    return x[-20:] + md5digest(x)


def md5digest(x):
    return hashlib.md5(x.encode("utf-8")).hexdigest()
