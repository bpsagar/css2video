import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Color, ColorParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Color.parse('#ffF')
        self.assertEqual(
            response,
            dict(type=ValueType.color, red=255, green=255, blue=255, alpha=1)
        )

        response = Color.parse('#FFFFFF')
        self.assertEqual(
            response,
            dict(type=ValueType.color, red=255, green=255, blue=255, alpha=1)
        )

        response = Color.parse('rgba(0, 0, 0, 1)')
        self.assertEqual(
            response,
            dict(type=ValueType.color, red=0, green=0, blue=0, alpha=1)
        )

        response = Color.parse('RGB(0, 0, 0)')
        self.assertEqual(
            response,
            dict(type=ValueType.color, red=0, green=0, blue=0, alpha=1)
        )

        with self.assertRaises(ColorParseException):
            Color.parse('#FFFF')

        with self.assertRaises(ColorParseException):
            Color.parse('rgb(0, 0, 0, 0.9')
