import json
import os.path
import pathlib
import tempfile

import pyfakefs

from vagrepo.repository import Repository

class RepositoryTestCase(pyfakefs.fake_filesystem_unittest.TestCase):
    '''Tests for vagrepo.cli.repository.Repository class'''

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

    def test_box_names(self):
        '''Test Repository class box_names property'''
        repo = Repository()

        user_1_box_1 = pathlib.Path(self.default_path, 'user_1', 'box_1')
        user_1_box_2 = pathlib.Path(self.default_path, 'user_1', 'box_2')
        anonymous_box = pathlib.Path(self.default_path, 'anonymous_box')

        for path in [user_1_box_1, user_1_box_2, anonymous_box]:
            path.mkdir(parents=True)
            pathlib.Path(path, 'metadata.json').touch()

        box_names = repo.box_names

        self.assertEqual(len(box_names), 3)
        self.assertIn('user_1/box_1', box_names)
        self.assertIn('user_1/box_2', box_names)
        self.assertIn('anonymous_box', box_names)

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
        metadata_path_2 = pathlib.Path(self.default_path, 'hello', 'world', 'metadata.json')
        self.assertTrue(pathlib.Path(self.default_path, 'hello', 'world').is_dir())
        self.assertTrue(metadata_path_2.is_file())
        with metadata_path_2.open() as fp_2:
            metadata_2 = json.load(fp_2)
        self.assertDictEqual(metadata_2, {'name': 'hello/world', "versions": []})

        repo.create('BOX_NAME', 'BOX_DESCRIPTION')
