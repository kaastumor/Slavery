import unittest
from tools.ci_scope import requires_database


class ScopeTests(unittest.TestCase):
    def test_research_only(self):
        self.assertFalse(requires_database(['experiments/exp04/packet.md', 'BACKLOG.md']))

    def test_mixed_and_unknown_changes_keep_database_gate(self):
        for path in ['db/migrations/0099.sql', 'tools/import_v061.py', 'compose.yaml',
                     'requirements.txt', 'tests/test_import_v061.py',
                     '.github/workflows/ci.yml', 'future_component/new_file', 'experiments/m2/check.sql', 'programmes/r1/build.py']:
            with self.subTest(path=path):
                self.assertTrue(requires_database(['docs/note.md', path]))

    def test_empty_diff_fails_closed(self):
        self.assertTrue(requires_database([]))
