__author__ = 'sami'

import unittest

from api import PushBullet


class PushTestCase(unittest.TestCase):

    def setUp(self):
        self.pb = PushBullet()

    def test_get_api_key(self):
        self.assertIsNotNone(
            self.pb.api_key
        )

    def test_set_api_key(self):
        key = self.pb.api_key
        self.pb.api_key = key
        self.assertEqual(
            key,
            self.pb.api_key
        )

    def test_current_user(self):
        user = self.pb.user
        self.assertIsNotNone(user['name'])
        self.assertIsNotNone(user['email'])
        self.assertIsNotNone(user['iden'])
