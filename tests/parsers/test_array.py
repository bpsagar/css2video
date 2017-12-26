import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Array, ArrayParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Array.parse('20px rgba(0, 0, 0, 1)')
        self.assertEqual(
            response,
            dict(type=ValueType.array, values=[
                dict(type=ValueType.length, value=20., unit='px'),
                dict(type=ValueType.color, red=0, green=0, blue=0, alpha=1)
            ])
        )

        with self.assertRaises(ArrayParseException):
            Array.parse('20px, 50px')
