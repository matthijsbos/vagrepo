import os.path
import pathlib

import pyfakefs

from vagrepo.repository import Repository

class RepositoryBoxNamesTestCase(pyfakefs.fake_filesystem_unittest.TestCase):
    '''
    Tests for vagrepo.cli.repository.Repository class. pyfakefs is used to
    mock the file system in order to isolate file system operations.
    '''

    def setUp(self):
        self.setUpPyfakefs()
        self.default_path = os.path.expanduser(os.path.join("~", ".vagrepo"))
        os.makedirs(self.default_path)

    def test_box_names(self):
        '''Test Repository class box_names property'''
        repo = Repository()

        user_1_box_1 = pathlib.Path(self.default_path, 'user_1-VAGRANTSLASH-box_1')
        user_1_box_2 = pathlib.Path(self.default_path, 'user_1-VAGRANTSLASH-box_2')
        anonymous_box = pathlib.Path(self.default_path, 'anonymous_box')

        for path in [user_1_box_1, user_1_box_2, anonymous_box]:
            path.mkdir(parents=True)
            pathlib.Path(path, 'metadata.json').touch()

        box_names = repo.box_names

        self.assertEqual(len(box_names), 3)
        self.assertIn('user_1/box_1', box_names)
        self.assertIn('user_1/box_2', box_names)
        self.assertIn('anonymous_box', box_names)
