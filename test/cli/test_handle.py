import unittest
import unittest.mock as mock

import vagrepo.cli

class HandleTestCase(unittest.TestCase):

    @mock.patch('vagrepo.cli.print_help')
    @mock.patch('vagrepo.repository.Repository')
    def test_handle_no_subcommand(self, mock_repo, mock_print_help):
        mock_namespace = mock.Mock()
        mock_namespace.subcommand = None

        vagrepo.cli.handle(mock_namespace)
        mock_print_help.assert_called_with()
        self.assertFalse(mock_repo.called)

    @mock.patch('vagrepo.cli.handle_list')
    @mock.patch('vagrepo.repository.Repository')
    def test_handle_list_subcommand(self, mock_repo, mock_list_handler):
        mock_repo_inst = mock.Mock()
        mock_repo.return_value = mock_repo_inst

        mock_namespace = mock.Mock()
        mock_namespace.subcommand = 'list'
        mock_namespace.path = None

        vagrepo.cli.handle(mock_namespace)
        mock_repo.assert_called_with(None)
        mock_list_handler.assert_called_with(mock_namespace, mock_repo_inst)
    
    @mock.patch('vagrepo.cli.handle_list')
    @mock.patch('vagrepo.repository.Repository')
    def test_handle_list_subcommand_with_custom_path(self, mock_repo, mock_list_handler):
        mock_repo_inst = mock.Mock()
        mock_repo.return_value = mock_repo_inst

        mock_path = mock.Mock()
        mock_namespace = mock.Mock()
        mock_namespace.subcommand = 'list'
        mock_namespace.path = mock_path

        vagrepo.cli.handle(mock_namespace)
        mock_repo.assert_called_with(mock_path)
        mock_list_handler.assert_called_with(mock_namespace, mock_repo_inst)
        