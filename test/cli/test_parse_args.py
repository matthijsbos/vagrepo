import unittest
import unittest.mock as mock
import sys

import vagrepo.cli

class ParseArgsTestCase(unittest.TestCase):
    def test_parse_args(self):
        test_args = "vagrepo list".split()
        with mock.patch('sys.argv', test_args):
            namespace = vagrepo.cli.parse_args()
            self.assertEqual(namespace.subcommand, "list")
            self.assertEqual(namespace.path, None)