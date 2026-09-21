import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"tools"))
from check_migration_ledger import compare, remote_names
class Tests(unittest.TestCase):
    def test_clean(self): self.assertEqual(compare(["0001_a"],["0001_a"])["missing_remote"],[])
    def test_irregular(self):
        r=compare(["0011_a","0012_b","0013_c","0014_d","0015_e"],["0011_a","0015_e","0015_e","0099_manual"])
        self.assertEqual(r["missing_remote"],["0012_b","0013_c","0014_d"]); self.assertEqual(r["duplicate_remote"],{"0015_e":2}); self.assertEqual(r["unknown_remote"],["0099_manual"])
    def test_supabase_shape(self): self.assertEqual(remote_names({"migrations":[{"version":"x","name":"0001_a"}]}),["0001_a"])
if __name__=="__main__": unittest.main()
