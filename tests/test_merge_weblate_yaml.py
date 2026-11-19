import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

from ruamel.yaml import YAML

SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'tools', 'merge-weblate-yaml.py')


class TestMergeWeblateYaml(unittest.TestCase):
    """Runs tools/merge-weblate-yaml.py the way the conflict workflow does."""

    def merge(self, base, ours, theirs, template=None):
        with tempfile.TemporaryDirectory() as tmp:
            def write(name, text):
                p = os.path.join(tmp, name)
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(textwrap.dedent(text))
                return p
            args = [sys.executable, SCRIPT]
            if template is not None:
                args += ['--template', write('en.yaml', template)]
            out = os.path.join(tmp, 'out.yaml')
            args += [write('base.yaml', base), write('ours.yaml', ours), write('theirs.yaml', theirs), out]
            result = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out, encoding='utf-8') as f:
                return f.read(), result.stderr

    def test_main_deletion_stays_deleted(self):
        out, notes = self.merge(
            base='a:\n    x: old\n    y: keep\n',
            ours='a:\n    y: keep\n',
            theirs='a:\n    x: translated\n    y: keep\n')
        self.assertNotIn('x:', out)
        self.assertIn('a.x', notes)

    def test_translator_addition_is_kept(self):
        out, notes = self.merge(
            base='a:\n    y: keep\n',
            ours='a:\n    y: keep\n',
            theirs='a:\n    y: keep\n    z: new\n')
        self.assertIn('z: new', out)
        self.assertEqual(notes, '')

    def test_one_sided_edits(self):
        out, _ = self.merge(
            base='a: 1\nb: 1\n',
            ours='a: main\nb: 1\n',
            theirs='a: 1\nb: weblate\n')
        self.assertIn('a: main', out)
        self.assertIn('b: weblate', out)

    def test_both_edited_main_wins_and_is_reported(self):
        out, notes = self.merge(base='a: old\n', ours='a: main\n', theirs='a: weblate\n')
        self.assertIn('a: main', out)
        self.assertIn('edited on both sides', notes)

    def test_both_added_main_wins_and_is_reported(self):
        out, notes = self.merge(base='{}\n', ours='a: main\n', theirs='a: weblate\n')
        self.assertIn('a: main', out)
        self.assertIn('written on both sides', notes)

    def test_weblate_dropping_a_key_keeps_main(self):
        out, _ = self.merge(base='a: 1\nb: 1\n', ours='a: 1\nb: 1\n', theirs='a: 1\n')
        self.assertIn('b: 1', out)

    def test_lists_are_not_merged_element_by_element(self):
        out, _ = self.merge(
            base='a:\n- 1\n- 2\n',
            ours='a:\n- 1\n- 2\n',
            theirs='a:\n- 1\n- 3\n')
        self.assertEqual(YAML(typ='safe').load(out), {'a': [1, 3]})

    def test_template_drops_keys_english_no_longer_has(self):
        # The language file never had level 4, so only the English file shows it is gone.
        out, notes = self.merge(
            template='dice:\n    levels:\n        3:\n            story_text: en\n',
            base='{}\n',
            ours='{}\n',
            theirs='dice:\n    levels:\n        3:\n            story_text: sk\n'
                   '        4:\n            story_text: sk4\n')
        self.assertIn('sk\n', out)
        self.assertNotIn('sk4', out)
        self.assertIn('dice.levels.4.story_text', notes)

    def test_empty_base_and_ours_for_a_new_language(self):
        out, _ = self.merge(base='', ours='', theirs='a: hello\n')
        self.assertIn('a: hello', out)

    def test_block_scalar_style_survives(self):
        theirs = 'a: |\n    line one\n    line two\nb: x\n'
        out, _ = self.merge(base='b: x\n', ours='b: x\n', theirs=theirs)
        self.assertIn('a: |\n', out)

    def test_merging_a_result_with_itself_changes_nothing(self):
        once, _ = self.merge(
            base='a:\n    x: 1\n\n    y: 2\n',
            ours='a:\n    x: main\n\n    y: 2\n',
            theirs='a:\n    x: 1\n\n    y: 2\n    z: new\n')
        twice, _ = self.merge(base=once, ours=once, theirs=once)
        self.assertEqual(once, twice)


if __name__ == '__main__':
    unittest.main()
