__author__ = 'sami'

import platform
import sys
import unittest

from bullet import main


class EndToEndTestCase(unittest.TestCase):

    def test_send_deployment_update(self):
        major, minor, _, _, _ = sys.version_info
        args = 'note all Unit tests running on {} Python {}.{}'.format(
            platform.system(),
            major,
            minor
        ).split(' ')
        main(args)
