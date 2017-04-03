import json
import os.path
import pathlib
import tempfile

import pyfakefs

from vagrepo.repository import Repository

class RepositoryInitTestCase(pyfakefs.fake_filesystem_unittest.TestCase):
    '''
    Tests for vagrepo.cli.repository.Repository class. pyfakefs is used to
    mock the file system in order to isolate file system operations.
    '''

    def setUp(self):
        self.setUpPyfakefs()
        self.default_path = os.path.expanduser(os.path.join("~", ".vagrepo"))
        os.makedirs(self.default_path)

    def test_init(self):
        '''Test Repository class constructor'''
        repo = Repository()
        self.assertEqual(repo.path, self.default_path)

        tmp_path = tempfile.mkdtemp()
        repo = Repository(path=tmp_path)
        self.assertEqual(repo.path, tmp_path)

        os.rmdir(tmp_path)
        self.assertFalse(os.path.exists(tmp_path))
        repo = Repository(path=tmp_path)
        self.assertTrue(os.path.exists(tmp_path))

        os.rmdir(tmp_path)
        self.assertFalse(os.path.exists(tmp_path))
        pathlib.Path(tmp_path).touch()
        with self.assertRaises(ValueError):
            Repository(path=tmp_path)
