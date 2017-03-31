import unittest
import unittest.mock as mock

import vagrepo.cli

class HandleCreateTestCase(unittest.TestCase):

    mock_namespace = mock.Mock()
    mock_repo = mock.Mock(spec=vagrepo.repository.Repository)

    vagrepo.cli.handle_add(mock_namespace, mock_repo)

    mock_repo.add.assert_called_with(mock_namespace.name, mock_namespace.file, mock_namespace.provider)