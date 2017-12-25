import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Length, LengthParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Length.parse('20px')
        self.assertEqual(
            response, dict(type=ValueType.length, value=20., unit='px')
        )

        response = Length.parse('-40.5EM')
        self.assertEqual(
            response, dict(type=ValueType.length, value=-40.5, unit='em')
        )

        with self.assertRaises(LengthParseException):
            Length.parse('20')

        with self.assertRaises(LengthParseException):
            Length.parse('20 px')
