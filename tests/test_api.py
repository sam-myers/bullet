__author__ = 'sami'

import unittest

from api import PushBullet


class PushBulletTestCase(unittest.TestCase):

    def setUp(self):
        self.pb = PushBullet()

    def test_get_api_key(self):
        self.assertIsNotNone(self.pb.api_key)

    def test_set_api_key(self):
        current_key = self.pb.api_key
        self.pb.api_key = 'test123'
        self.assertEqual('test123', self.pb.api_key)
        self.pb.api_key = current_key

    def test_current_user(self):
        user = self.pb.user
        self.assertIsNotNone(user['name'])
        self.assertIsNotNone(user['email'])
        self.assertIsNotNone(user['iden'])
