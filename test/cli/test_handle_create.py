import unittest
import unittest.mock as mock

import vagrepo.cli
import vagrepo.repository

class HandleCreateTestCase(unittest.TestCase):

    def test_handle_create(self):
        '''test vagrepo.cli.handle_create'''
        mock_namespace = mock.Mock()
        mock_repository = mock.Mock(spec=vagrepo.repository.Repository)

        vagrepo.cli.handle_create(mock_namespace, mock_repository)
        mock_repository.create.assert_called_with(mock_namespace.name, mock_namespace.description)

