import unittest
from uuid import NAMESPACE_URL, uuid5

from tools import export_geometry_closure_tranche_02_sql as exporter
from tools import rehearse_geometry_closure_tranche_02 as rehearsal
from tools.rehearse_geometry_closure_tranche_01 import ClosureError


class ConnectedSqlExportTests(unittest.TestCase):
    def test_default_export_is_inert_and_symbols_never_escape(self):
        statement = exporter.render(rehearsal.load_review(), revision='UNIT_TEST')
        self.assertIn("IF NOT (false) THEN RAISE EXCEPTION", statement)
        self.assertLess(statement.index('authorization absent'), statement.index('insert into'))
        for i in range(20):
            self.assertNotIn(str(uuid5(NAMESPACE_URL, f'atlas/374/export/generated_{i}')), statement)
        self.assertNotIn('DATABASE_URL', statement)
        self.assertNotIn('COMMIT', statement)

    def test_unrecognized_helper_lookup_fails_closed(self):
        with self.assertRaises(ClosureError):
            exporter.InsertCollector().execute('select * from atlas.claim')

    def test_parameter_literals_preserve_quotes_and_backslashes(self):
        collector = exporter.InsertCollector()
        collector.execute('insert into atlas.source(title) values (%s) returning source_id',
                          ("source's \\ path; SELECT 1;",))
        statement = collector.statements[0]
        self.assertIn("source''s", statement)
        self.assertIn('INTO generated_0', statement)


if __name__ == '__main__':
    unittest.main()
