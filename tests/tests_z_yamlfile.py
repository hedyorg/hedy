import os
import time
import unittest

from website.yaml_file import YamlFile


class TestYamlFile(unittest.TestCase):
    def test_load_yaml_equivalent(self):
        """Test that when we load a YAML file uncached and cached, it produces the same data.

        Also get a gauge for the speedup we get from loading a pickled file,
        although we're not going to fail the test on the numbers we get from that.
        """
        n = 10

        # Pick a file with unicode in it so we're sure it gets handled properly
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        yaml_file = os.path.normpath(root_dir + '/content/adventures/hu.yaml')
        file = YamlFile(yaml_file)

        # Remove pickled version of this file if it exists, it may
        # influence the tests
        if os.path.isfile(file.pickle_filename):
            os.unlink(file.pickle_filename)

        start = time.time()
        for _ in range(n):
            original_data = file.load_uncached()
        original_seconds = time.time() - start

        # Generate the pickle file
        file.access()

        start = time.time()
        for _ in range(n):
            cached_data = file.load_pickle()
        cached_seconds = time.time() - start

        self.assertEqual(original_data, cached_data)
        print(
            f'YAML loading takes {original_seconds / n} seconds, unpickling takes {cached_seconds / n}'
            f'({original_seconds / cached_seconds:.1f}x faster)')
