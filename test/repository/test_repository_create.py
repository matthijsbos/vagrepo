import json
import os.path
import pathlib

import pyfakefs

from vagrepo.repository import Repository

class RepositoryCreateTestCase(pyfakefs.fake_filesystem_unittest.TestCase):
    '''
    Tests for vagrepo.cli.repository.Repository class. pyfakefs is used to
    mock the file system in order to isolate file system operations.
    '''

    def setUp(self):
        self.setUpPyfakefs()
        self.default_path = os.path.expanduser(os.path.join("~", ".vagrepo"))
        os.makedirs(self.default_path)

    def test_create(self):
        '''Test Repository class create method'''
        repo = Repository()

        repo.create('ubuntu_16_04_x64')
        metadata_path_1 = pathlib.Path(self.default_path, 'ubuntu_16_04_x64', 'metadata.json')
        self.assertTrue(pathlib.Path(self.default_path, 'ubuntu_16_04_x64').is_dir())
        self.assertTrue(metadata_path_1.is_file())
        with metadata_path_1.open() as fp_1:
            metadata_1 = json.load(fp_1)
        self.assertDictEqual(metadata_1, {'name': 'ubuntu_16_04_x64', "versions": []})

        repo.create('hello/world')
        metadata_path_2 = pathlib.Path(self.default_path, \
                                       'hello-VAGRANTSLASH-world', \
                                       'metadata.json')
        self.assertTrue(pathlib.Path(self.default_path, 'hello-VAGRANTSLASH-world').is_dir())
        self.assertTrue(metadata_path_2.is_file())
        with metadata_path_2.open() as fp_2:
            metadata_2 = json.load(fp_2)
        self.assertDictEqual(metadata_2, {'name': 'hello/world', "versions": []})

        repo.create('BOX_NAME', 'BOX_DESCRIPTION')

    def test_create_raises(self):
        repo = Repository()

        repo.create('some/repo')
        repo.create('some/other_repo')

        with self.assertRaises(ValueError):
            repo.create('some/repo')
