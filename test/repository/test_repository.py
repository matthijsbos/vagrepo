import json
import os.path
import pathlib
import tempfile
import unittest.mock as mock

import pyfakefs

from vagrepo.repository import Repository

class RepositoryTestCase(pyfakefs.fake_filesystem_unittest.TestCase):
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

    @mock.patch('hashlib.sha1')
    def test_add(self, mock_sha1):
        '''Test Repository class add method'''

        mock_sha1_inst = mock.Mock()
        mock_sha1_inst.hexdigest.return_value = 'HASH'
        mock_sha1.return_value = mock_sha1_inst

        box_dir = pathlib.Path(self.default_path, 'some', 'box')
        box_meta_path = pathlib.Path(box_dir, 'metadata.json')
        box_meta_json = {
            "name": "some/box",
            "versions": []
        }

        box_name = 'some/box'
        box_file_src = pathlib.Path('~', 'Downloads', 'some_box_file.box')
        box_version = '0.1.0'
        box_provider = 'virtualbox'

        real_file_src = pathlib.Path(pathlib.Path(__file__).parent, 'resources', 'empty_boxes', 'virtualbox', 'empty_virtualbox.tar.box')
        self.copyRealFile(str(real_file_src), str(box_file_src))

        box_file_dest = pathlib.Path(box_dir, box_version, box_provider + '.box')

        # initialize test environment, manually create empty box
        box_dir.mkdir(parents=True)
        with box_meta_path.open('w') as box_meta_fp:
            json.dump(box_meta_json, box_meta_fp)

        repo = Repository()
        repo.add(box_name, box_file_src, box_version, box_provider)

        with box_meta_path.open() as box_meta_fp:
            add_meta_json = json.load(box_meta_fp)

        self.assertTrue(box_file_dest.exists())
        self.assertDictEqual(add_meta_json, {
            "name": "some/box",
            "versions": [
                {
                    "version": "0.1.0",
                    "providers": [
                        {
                            "name": "virtualbox",
                            "url": box_file_dest.as_uri(),
                            "checksum_type": "sha1",
                            "checksum": 'HASH'
                        }
                    ]
                }
            ]
        })


