__author__ = 'sami'

from io import StringIO
import sys
import unittest
from unittest.mock import MagicMock

from api import PushBullet
from bullet import main, prompt_for_api_key


class MainTestCase(unittest.TestCase):

    def test_invalid_command(self):
        out = StringIO()
        sys.stdout = out
        args = 'non_existent_command and some other stuff'.split(' ')
        main(args)
        output = out.getvalue().strip()
        self.assertTrue('Unknown command' in output)

    def test_invalid_device(self):
        out = StringIO()
        sys.stdout = out
        args = 'note foobar invalid recipient device'.split(' ')
        main(args)
        output = out.getvalue().strip()
        self.assertTrue('Device name not recognized' in output)

    def test_help_message(self):
        out = StringIO()
        sys.stdout = out
        args = 'help'.split(' ')
        main(args)
        output = out.getvalue().strip()
        self.assertTrue('Valid commands:' in output)
