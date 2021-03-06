import unittest
import unittest.mock as mock

import vagrepo.cli

class ParseArgsTestCase(unittest.TestCase):
    '''Tests for vagrepo.cli.parse_args'''

    def test_parse_list(self):
        '''Test parsing of arguments with the list subcommand'''
        test_args = "vagrepo list".split()
        with mock.patch('sys.argv', test_args):
            namespace = vagrepo.cli.parse_args()
            self.assertEqual(namespace.subcommand, "list")
            self.assertEqual(namespace.path, None)

    def test_parse_create(self):
        '''Test parsing of arguments with the create subcommand'''
        test_args_1 = 'vagrepo create USER_NAME/BOX_NAME'.split()
        with mock.patch('sys.argv', test_args_1):
            namespace = vagrepo.cli.parse_args()
            self.assertEqual(namespace.subcommand, 'create')
            self.assertEqual(namespace.path, None)
            self.assertEqual(namespace.name, 'USER_NAME/BOX_NAME')
            self.assertEqual(namespace.description, None)

        test_args_2 = 'vagrepo create NAME --description DESCRIPTION'.split()
        with mock.patch('sys.argv', test_args_2):
            namespace = vagrepo.cli.parse_args()
            self.assertEqual(namespace.name, 'NAME')
            self.assertEqual(namespace.description, 'DESCRIPTION')

        test_args_3 = 'vagrepo create --description=DESCRIPTION    NAME '.split()
        with mock.patch('sys.argv', test_args_3):
            namespace = vagrepo.cli.parse_args()
            self.assertEqual(namespace.subcommand, 'create')
            self.assertEqual(namespace.name, 'NAME')
            self.assertEqual(namespace.description, 'DESCRIPTION')

        test_args_4 = 'vagrepo --path /some/path create HELLO --description WORLD '.split()
        with mock.patch('sys.argv', test_args_4):
            namespace = vagrepo.cli.parse_args()
            self.assertEqual(namespace.name, 'HELLO')
            self.assertEqual(namespace.description, 'WORLD')
            self.assertEqual(namespace.subcommand, 'create')
            self.assertEqual(namespace.path, '/some/path')

    def test_parse_add(self):
        '''Test parsing of arguments for the add subcommand'''
        test_args_1 = 'vagrepo add user/box some_file.box'.split()
        with mock.patch('sys.argv', test_args_1):
            namespace_1 = vagrepo.cli.parse_args()
            self.assertEqual(namespace_1.subcommand, 'add')
            self.assertEqual(namespace_1.path, None)
            self.assertEqual(namespace_1.name, 'user/box')
            self.assertEqual(namespace_1.file, 'some_file.box')
            self.assertEqual(namespace_1.provider, None)

        test_args_2 = 'vagrepo add user/box some_file.box --provider virtualbox'.split()
        with mock.patch('sys.argv', test_args_2):
            namespace_2 = vagrepo.cli.parse_args()
            self.assertEqual(namespace_2.subcommand, 'add')
            self.assertEqual(namespace_2.path, None)
            self.assertEqual(namespace_2.name, 'user/box')
            self.assertEqual(namespace_2.file, 'some_file.box')
            self.assertEqual(namespace_2.provider, 'virtualbox')
