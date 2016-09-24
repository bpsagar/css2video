import unittest

from css2video.parsers import parse_value
from .utils import isEqual


class TestParser(unittest.TestCase):
    '''Parser tests'''

    def test_value(self):
        '''Tests all types of CSS property values'''
        value_data = {
            '100': {
                'type': 'number',
                'value': 100
            },
            '12.5': {
                'type': 'number',
                'value': 12.5
            },
            '20px': {
                'type': 'length',
                'value': 20,
                'unit': 'px'
            },
            '10%': {
                'type': 'percentage',
                'value': 10
            },
            '0.3s': {
                'type': 'time',
                'value': 0.3
            },
            'rgba(0, 0, 0, 1)': {
                'type': 'color',
                'red': 0,
                'green': 0,
                'blue': 0,
                'alpha': 1
            },
            '#FFF': {
                'type': 'color',
                'red': 255,
                'green': 255,
                'blue': 255,
                'alpha': 1
            },
            'translateX(20px 2s)': {
                'type': 'function',
                'name': 'translateX',
                'args': [
                    {
                        'type': 'length',
                        'value': 20,
                        'unit': 'px'
                    },
                    {
                        'type': 'time',
                        'value': 2
                    },
                ]
            },
            '20px rgba(255, 255, 255, 1)': {
                'type': 'array',
                'values': [
                    {
                        'type': 'length',
                        'value': 20,
                        'unit': 'px'
                    },
                    {
                        'type': 'color',
                        'red': 255,
                        'green': 255,
                        'blue': 255,
                        'alpha': 1
                    }
                ]
            },
            '"http://www.google.com"': {
                'type': 'url',
                'value': '"http://www.google.com"'
            }
        }
        for value, expected_parsed_value in value_data.items():
            parsed_value = parse_value(value)
            self.assertTrue(isEqual(parsed_value, expected_parsed_value))
