import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Number, NumberParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Number.parse('20')
        self.assertEqual(response, dict(type=ValueType.number, value=20.))

        response = Number.parse('+1')
        self.assertEqual(response, dict(type=ValueType.number, value=1.))

        response = Number.parse('-20.5')
        self.assertEqual(response, dict(type=ValueType.number, value=-20.5))

        with self.assertRaises(NumberParseException):
            Number.parse('ab')

        with self.assertRaises(NumberParseException):
            response = Number.parse('20.4.2')
