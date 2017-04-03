import json
import os.path
import pathlib
import unittest.mock as mock

import pyfakefs

from vagrepo.repository import Repository

class RepositoryAddTestCase(pyfakefs.fake_filesystem_unittest.TestCase):
    '''
    Tests for vagrepo.cli.repository.Repository class. pyfakefs is used to
    mock the file system in order to isolate file system operations.
    '''

    def setUp(self):
        self.setUpPyfakefs()
        self.default_path = os.path.expanduser(os.path.join("~", ".vagrepo"))
        os.makedirs(self.default_path)

    @mock.patch('hashlib.sha1')
    def test_add(self, mock_sha1):
        '''Test Repository class add method'''

        mock_sha1_inst = mock.Mock()
        mock_sha1_inst.hexdigest.return_value = 'HASH'
        mock_sha1.return_value = mock_sha1_inst

        box_dir = pathlib.Path(self.default_path, 'some-VAGRANTSLASH-box')
        box_meta_path = pathlib.Path(box_dir, 'metadata.json')
        box_meta_json = {
            "name": "some/box",
            "versions": []
        }

        box_name = 'some/box'
        box_file_src = pathlib.Path('~', 'Downloads', 'some_box_file.box')
        box_version = '0.1.0'
        box_provider = 'virtualbox'

        real_file_src = pathlib.Path(pathlib.Path(__file__).parent, \
                                     'resources', 'empty_boxes', 'virtualbox', \
                                     'empty_virtualbox.tar.box')
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


