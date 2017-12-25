import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Time, TimeParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Time.parse('20s')
        self.assertEqual(
            response, dict(type=ValueType.time, value=20.)
        )

        response = Time.parse('-40.5S')
        self.assertEqual(
            response, dict(type=ValueType.time, value=-40.5)
        )

        with self.assertRaises(TimeParseException):
            Time.parse('20')

        with self.assertRaises(TimeParseException):
            Time.parse('20 s')
