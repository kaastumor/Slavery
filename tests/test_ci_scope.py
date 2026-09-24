import unittest
from tools.ci_scope import requires_database


class ScopeTests(unittest.TestCase):
    def test_research_only(self):
        self.assertFalse(requires_database(['experiments/exp04/packet.md', 'BACKLOG.md']))

    def test_frontend_only_uses_web_workflow_not_postgis(self):
        paths = [
            'web/src/research-preview.ts',
            'web/src/research-preview.css',
            'web/public/data/exp04-research-preview.json',
            'web/package-lock.json',
            'web/vite.config.ts',
            'tools/build_exp04_research_preview.py',
            'tools/build_exp06_candidate.py',
            '.github/workflows/web-mvp.yml',
        ]
        self.assertFalse(requires_database(paths))

    def test_ci_scope_unit_change_is_non_database(self):
        self.assertFalse(requires_database(['tools/ci_scope.py', 'tests/test_ci_scope.py']))

    def test_mixed_and_unknown_changes_keep_database_gate(self):
        for path in [
            'db/migrations/0099.sql',
            'tools/import_v061.py',
            'compose.yaml',
            'requirements.txt',
            'tests/test_import_v061.py',
            '.github/workflows/ci.yml',
            'future_component/new_file',
            'experiments/m2/check.sql',
            'programmes/r1/build.py',
        ]:
            with self.subTest(path=path):
                self.assertTrue(requires_database(['docs/note.md', path]))

    def test_empty_diff_fails_closed(self):
        self.assertTrue(requires_database([]))


if __name__ == '__main__':
    unittest.main()
