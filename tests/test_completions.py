import unittest

from completer import CommandCompleter
from api import PushBullet


class CompleterTestCase(unittest.TestCase):

    def setUp(self):
        self.pushbullet = PushBullet()
        self.completer = CommandCompleter(self.pushbullet)

    def test_command_list(self):
        document = MockDocument('')
        words = [i.text for i in self.completer.get_completions(document, None)]
        self.assertIn('help', words)
        self.assertIn('quit', words)
        self.assertIn('note', words)
        self.assertIn('link', words)
        self.assertIn('devices', words)

    def test_device_list(self):
        document = MockDocument('note ')
        words = [i.text for i in self.completer.get_completions(document, None)]
        devices = [i.name.lower() for i in self.pushbullet.devices]
        for d in devices:
            self.assertIn(d, words)
        self.assertIn('all', words)

    def test_device_list_partial_match(self):
        document = MockDocument('note al')
        words = [i.text for i in self.completer.get_completions(document, None)]
        self.assertIn('all', words)
        self.assertLess(len(words), len(self.pushbullet.devices))

    def test_note_message(self):
        document = MockDocument('note all dsfewfg')
        words = [i.display for i in self.completer.get_completions(document, None)]
        self.assertEqual(['Message to push'], words)

    def test_link_url_message(self):
        document = MockDocument('link all http://xkcd')
        words = [i.display for i in self.completer.get_completions(document, None)]
        self.assertEqual(['URL to push'], words)

    def test_link_url_optional_body(self):
        document = MockDocument('link all http://xkcd.com ')
        words = [i.display for i in self.completer.get_completions(document, None)]
        self.assertEqual(['[Optional] Message to push'], words)


class MockDocument(object):

    def __init__(self, line):
        self.current_line = line

    def get_word_before_cursor(self):
        """
        Give the word before the cursor.
        If we have whitespace before the cursor this returns an empty string.
        """
        if self.current_line[-1:].isspace():
            return ''
        else:
            return self.current_line.split(' ')[-1]
