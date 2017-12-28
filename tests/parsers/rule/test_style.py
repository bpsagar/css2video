import unittest

from css2video.constants import RuleType, ValueType
from css2video.parsers.rule import Style, StyleParseException


class TestCase(unittest.TestCase):
    def test_parser(self):
        response = Style.parse('div { margin: 20px; }')
        self.assertEqual(response['type'], RuleType.style)
        self.assertEqual(response['selector'], 'div')
        self.assertEqual(response['properties'], [
            dict(
                property_name='margin',
                property_value=dict(
                    type=ValueType.length, value=20., unit='px'
                )
            )
        ])

        with self.assertRaises(StyleParseException):
            Style.parse('div { ; }')
