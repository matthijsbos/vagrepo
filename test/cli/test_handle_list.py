import io
import unittest
import unittest.mock as mock

import vagrepo.cli

class HandleListTestCase(unittest.TestCase):
    '''Tests for vagrepo.cli.handle_list function'''

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_list(self, mock_stdout):

        mock_namespace = mock.Mock()
        mock_repo = mock.Mock()
        mock_repo.box_names = ['hello', 'world']
        vagrepo.cli.handle_list(mock_namespace, mock_repo)

        self.assertIn('hello', mock_stdout.getvalue())
        self.assertIn('world', mock_stdout.getvalue())
