import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Url, UrlParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Url.parse('"http://www.google.com"')
        self.assertEqual(
            response,
            dict(type=ValueType.url, value='"http://www.google.com"')
        )

        with self.assertRaises(UrlParseException):
            Url.parse('random-text')
