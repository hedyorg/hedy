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

    # Merging of YAML content
    # Key of type dict
    def test_merge_dicts_prefers_source(self):
        result = YamlFile.merge_yaml({"key1": "source"}, {"key1": "fallback"})
        self.assertEqual({"key1": "source"}, result)

    def test_merge_dicts_uses_fallback_if_source_key_not_present(self):
        result = YamlFile.merge_yaml({}, {"key1": "fallback"})
        self.assertEqual({"key1": "fallback"}, result)

    def test_merge_dicts_skips_key_if_not_present_in_fallback_empty(self):
        result = YamlFile.merge_yaml({"key1": "source"}, {})
        self.assertEqual({}, result)

    def test_merge_dicts_skips_key_if_not_present_in_fallback(self):
        result = YamlFile.merge_yaml({"key2": "source"}, {"key1": "fallback"})
        self.assertEqual({"key1": "fallback"}, result)

    # Key of type list
    def test_merge_lists_prefers_source(self):
        result = YamlFile.merge_yaml({"key1": ["a", "b"]}, {"key1": ["c", "d"]})
        self.assertEqual({"key1": ["a", "b"]}, result)

    def test_merge_lists_skips_key_if_not_present_in_fallback(self):
        result = YamlFile.merge_yaml({"key1": ["a", "b"]}, {})
        self.assertEqual({}, result)

    def test_merge_lists_uses_fallback_if_source_key_not_present_empty(self):
        result = YamlFile.merge_yaml({}, {"key1": ["c", "d"]})
        self.assertEqual({"key1": ["c", "d"]}, result)

    def test_merge_lists_uses_fallback_if_source_key_not_present(self):
        result = YamlFile.merge_yaml({"key2": ["a", "b"]}, {"key1": ["c", "d"]})
        self.assertEqual({"key1": ["c", "d"]}, result)

    # Elements in list
    def test_merge_lists_values_prefers_source(self):
        result = YamlFile.merge_yaml({"key1": [None, "b"]}, {"key1": ["c", "d"]})
        self.assertEqual({"key1": ["c", "b"]}, result)

    def test_merge_lists_values_uses_fallback_if_value_is_empty(self):
        result = YamlFile.merge_yaml({"key1": ["", "b"]}, {"key1": ["c", "d"]})
        self.assertEqual({"key1": ["c", "b"]}, result)

    def test_merge_lists_values_prefers_len_of_fallback(self):
        result = YamlFile.merge_yaml({"key1": ["a", "b", "e"]}, {"key1": ["c", "d"]})
        self.assertEqual({"key1": ["a", "b"]}, result)

    def test_merge_lists_values_prefers_source_values(self):
        result = YamlFile.merge_yaml({"key1": ["a"]}, {"key1": ["c", "d"]})
        self.assertEqual({"key1": ["a", "d"]}, result)

    # Keys with mismatched types
    def test_merge_dicts_prefers_fallback_type_dict(self):
        result = YamlFile.merge_yaml({"key1": ["a", "b"]}, {"key1": {"a": "c", "b": "d"}})
        self.assertEqual({"key1": {"a": "c", "b": "d"}}, result)

    def test_merge_dicts_prefers_fallback_type_str(self):
        result = YamlFile.merge_yaml({"key1": ["a", "b"]}, {"key1": "string value"})
        self.assertEqual({"key1": "string value"}, result)

    def test_merge_dicts_prefers_fallback_type_list(self):
        result = YamlFile.merge_yaml({"key1": {"a": "c", "b": "d"}}, {"key1": ["a", "b"]})
        self.assertEqual({"key1": ["a", "b"]}, result)

    def test_merge_dicts_prefers_fallback_type_string(self):
        result = YamlFile.merge_yaml({"key1": {"a": "c", "b": "d"}}, {"key1": "string value"})
        self.assertEqual({"key1": "string value"}, result)

    def test_merge_dicts_prefers_fallback_type_bool(self):
        result = YamlFile.merge_yaml({"key1": True}, {"key1": "string value"})
        self.assertEqual({"key1": True}, result)
