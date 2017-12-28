import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Percentage, PercentageParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Percentage.parse('20%')
        self.assertEqual(
            response, dict(type=ValueType.percentage, value=20.)
        )

        response = Percentage.parse('-40.5%')
        self.assertEqual(
            response, dict(type=ValueType.percentage, value=-40.5)
        )

        with self.assertRaises(PercentageParseException):
            Percentage.parse('20')

        with self.assertRaises(PercentageParseException):
            Percentage.parse('20 %')
