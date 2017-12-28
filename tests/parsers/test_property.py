import unittest

from css2video.constants import ValueType
from css2video.parsers.property import Property, PropertyParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Property.parse('margin: 20px;')
        self.assertEqual(response['property_name'], 'margin')
        self.assertEqual(response['property_value'], dict(
            type=ValueType.length, value=20., unit='px'
        ))

        response = Property.parse(' background-color : #FFF ;')
        self.assertEqual(response['property_name'], 'background-color')
        self.assertEqual(response['property_value'], dict(
            type=ValueType.color, red=255, green=255, blue=255, alpha=1
        ))

        with self.assertRaises(PropertyParseException):
            Property.parse('rand-adb:- 20px')
