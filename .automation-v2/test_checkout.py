import base64
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import checkout as c

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cache = self.root/'blobs';self.cache.mkdir()
        self.files = [('data.txt', b'hello\r\nworld\n','100644'), ('bin/run',b'#!/bin/sh\nexit 0\n','100755'), ('bytes.bin',bytes(range(256)),'100644'), ('.gitignore',b'data.txt\n','100644')]
        self.entries=[]
        for path,raw,mode in self.files:
            sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            self.entries.append(dict(path=path,sha=sha,type='blob',mode=mode,size=len(raw)))
            (self.cache/(sha+'.json')).write_text(json.dumps(dict(sha=sha,encoding='base64',size=len(raw),content=base64.b64encode(raw).decode())))
        # Use Git as an independent tree oracle including nested dirs and modes.
        oracle=self.root/'oracle';oracle.mkdir();c.run(oracle,'init','--quiet')
        for e,(_,raw,_) in zip(self.entries,self.files):
            sha=c.run(oracle,'hash-object','-w','--stdin',data=raw)
            c.run(oracle,'update-index','--add','--cacheinfo',e['mode'],sha,e['path'])
        self.manifest=dict(repository='kaastumor/morrow-needle',revision='a'*40,tree_sha=c.run(oracle,'write-tree'),truncated=False,tree=self.entries)
    def tearDown(self):self.temp.cleanup()
    def call(self):return c.materialize(self.manifest,self.cache,self.root/'checkout')
    def test_exact_binary_newline_modes_and_ignored_files(self):
        result=self.call();self.assertTrue(result['clean']);self.assertEqual(result['verified_tree'],self.manifest['tree_sha'])
        for path,raw,mode in self.files:
            p=self.root/'checkout'/path;self.assertEqual(p.read_bytes(),raw);self.assertEqual(bool(p.stat().st_mode&0o111),mode=='100755')
        self.assertEqual(result['history'],'NOT_RECONSTRUCTED')
    def test_corrupt_blob_prevents_destination_creation(self):
        sha=self.entries[0]['sha'];p=self.cache/(sha+'.json');b=json.loads(p.read_text());b['content']=base64.b64encode(b'wrong').decode();p.write_text(json.dumps(b))
        with self.assertRaises(ValueError):self.call()
        self.assertFalse((self.root/'checkout').exists())
    def test_truncated_tree_rejected(self):
        self.manifest['truncated']=True
        with self.assertRaisesRegex(ValueError,'TRUNCATED_TREE'):self.call()
    def test_wrong_tree_rejected(self):
        self.manifest['tree_sha']='b'*40
        with self.assertRaisesRegex(ValueError,'TREE_HASH_MISMATCH'):self.call()
    def test_traversal_and_git_internal_paths_rejected(self):
        for p in ['../secret','/absolute','a/../secret','.git/config','a//b']:
            with self.subTest(path=p):
                self.entries[0]['path']=p
                with self.assertRaisesRegex(ValueError,'UNSAFE_PATH'):self.call()
    def test_symlink_and_submodule_fail_closed(self):
        self.entries[0]['mode']='120000'
        with self.assertRaisesRegex(ValueError,'UNSUPPORTED_MODE'):self.call()
    def test_duplicate_path_rejected(self):
        self.entries.append(self.entries[0])
        with self.assertRaisesRegex(ValueError,'DUPLICATE_PATH'):self.call()
    def test_existing_destination_never_overwritten(self):
        dest=self.root/'checkout';dest.mkdir();(dest/'keep').write_text('existing')
        with self.assertRaisesRegex(ValueError,'DESTINATION_EXISTS'):self.call()
        self.assertEqual((dest/'keep').read_text(),'existing')
    def test_utf8_fallback_preserves_exact_original_bytes(self):
        for e,(_,raw,_) in zip(self.entries,self.files):
            if e['path']=='bytes.bin':continue
            (self.cache/(e['sha']+'.json')).write_text(json.dumps(dict(sha=e['sha'],encoding='utf-8',size=len(raw),content=raw.decode('utf-8'))))
        self.assertTrue(self.call()['clean'])

if __name__=='__main__':unittest.main(verbosity=2)
