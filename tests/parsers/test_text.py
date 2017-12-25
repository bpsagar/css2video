import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Text, TextParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Text.parse('inline-block')
        self.assertEqual(
            response, dict(type=ValueType.text, value='inline-block'))

        with self.assertRaises(TextParseException):
            Text.parse('inline block')
