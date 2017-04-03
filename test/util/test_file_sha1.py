import pathlib
import unittest

import vagrepo.util

class Sha1TestCase(unittest.TestCase):

    def test_sha1(self):
        script_dir = pathlib.Path(__file__).parent
        resources_dir = pathlib.Path(script_dir, 'resources')
        # Test files contain random data. Test hashes were generated using
        # Ubuntu's sha1sum utility.
        file_0_path = pathlib.Path(resources_dir, '0.random')
        file_0_sha1 = 'f342c90274b93a84595ea99f949786e415759c59'
        file_1_path = pathlib.Path(resources_dir, '1.random')
        file_1_sha1 = '0c74ea5adaf8f8d47a70ac4000af3d4668dece50'
        file_2_path = pathlib.Path(resources_dir, '2.random')
        file_2_sha1 = 'f87bd86590ed9fa2c93126f8a0c581425a5db7c7'

        self.assertEqual(vagrepo.util.file_sha1(file_0_path), file_0_sha1)
        self.assertEqual(vagrepo.util.file_sha1(file_1_path), file_1_sha1)
        self.assertEqual(vagrepo.util.file_sha1(file_2_path), file_2_sha1)

