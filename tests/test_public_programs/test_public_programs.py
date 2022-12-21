import json
import unittest
from tests.Tester import HedyTester, Snippet
from parameterized import parameterized

most_recent_file_name = 'tests/test_public_programs/filtered-programs-2022-12-01.json'
public_snippets = []

# this file tests all public programs in the database
# while saving, they were not broken (no Parse error or other Hedy exception)
# these tests make sure we aren't accidentally breaking public programs

with open(most_recent_file_name, 'r') as public_programs_file:
    text = public_programs_file.read()
    public_programs = json.loads(text)

for p in public_programs:
    s = Snippet(filename='file',
                level=int(p['level']),
                field_name='field',
                code=p['code'],
                language=p['language'],
                error=p['error']
                )
    public_snippets.append(s)

p2 = [(s.name, s) for s in public_snippets]


class TestsPublicPrograms(unittest.TestCase):
    @parameterized.expand(p2)
    def test_programs(self, name, snippet):
        if snippet is not None and not snippet.error:
            print(snippet.code)
            result = HedyTester.check_Hedy_code_for_errors(snippet)
            self.assertIsNone(result)
