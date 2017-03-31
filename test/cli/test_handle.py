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

    @mock.patch('vagrepo.cli.handle_add')
    @mock.patch('vagrepo.cli.handle_create')
    @mock.patch('vagrepo.cli.handle_list')
    @mock.patch('vagrepo.repository.Repository')
    def test_handle_subcommands(self, mock_repo, mock_handle_list, 
        mock_handle_create, mock_handle_add):
        '''Test the proper transfer to a subcommand's corresponding handler'''
        mapping = {
            'list': mock_handle_list,
            'create': mock_handle_create,
            'add': mock_handle_add
        }
        # Test without custom path
        for subcommand, mock_handler in mapping.items():
            mock_repo_inst = mock.Mock()
            mock_repo.return_value = mock_repo_inst
            mock_namespace = mock.Mock()
            mock_namespace.subcommand = subcommand
            mock_namespace.path = None

            vagrepo.cli.handle(mock_namespace)

            mock_repo.assert_called_with(None)
            mock_handler.assert_called_with(mock_namespace, mock_repo_inst)

        # Test with a custom repository path set
        for subcommand, mock_handler in mapping.items():
            mock_repo_inst = mock.Mock()
            mock_repo.return_value = mock_repo_inst
            mock_namespace = mock.Mock()
            mock_namespace.subcommand = subcommand

            vagrepo.cli.handle(mock_namespace)

            mock_repo.assert_called_with(mock_namespace.path)
            mock_handler.assert_called_with(mock_namespace, mock_repo_inst)

