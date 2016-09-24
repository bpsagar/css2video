import unittest

from css2video.parsers import parse_property
from css2video.parsers import parse_rule
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

    def test_property(self):
        property_data = [
            (
                'background-color: rgba(0, 0, 0, 0.5);',
                {
                    'property_name': 'background-color',
                    'property_value': {
                        'type': 'color',
                        'red': 0,
                        'green': 0,
                        'blue': 0,
                        'alpha': 0.5
                    }
                }
            ),
            (
                'box-shadow: 0px 0px 4px #000;',
                {
                    'property_name': 'box-shadow',
                    'property_value': {
                        'type': 'array',
                        'values': [
                            {
                                'type': 'length',
                                'value': 0,
                                'unit': 'px'
                            },
                            {
                                'type': 'length',
                                'value': 0,
                                'unit': 'px'
                            },
                            {
                                'type': 'length',
                                'value': 4,
                                'unit': 'px'
                            },
                            {
                                'type': 'color',
                                'red': 0,
                                'green': 0,
                                'blue': 0,
                                'alpha': 1
                            }
                        ]
                    }
                }
            )
        ]
        for property, expected_parsed_property in property_data:
            parsed_property = parse_property(property)
            self.assertTrue(parsed_property, expected_parsed_property)

    def test_rule(self):
        rule_data = [
            (
                'div{margin-top: 20px;}',
                {
                    'type': 'style',
                    'selector': 'div',
                    'properties': [
                        {
                            'property_name': 'margin-top',
                            'property_value': {
                                'type': 'length',
                                'value': 20,
                                'unit': 'px'
                            }
                        }
                    ]
                }
            ),
            (
                '''
                @keyframes mymove {
                    from {top: 0px;}
                    to {top: 200px;}
                }
                ''',
                {
                    'type': 'keyframes',
                    'name': 'mymove',
                    'keyframes': [
                        {
                            'keyframe_selector': 0,
                            'properties': [
                                {
                                    'property_name': 'top',
                                    'property_value': {
                                        'type': 'length',
                                        'value': 0,
                                        'unit': 'px'
                                    }
                                }
                            ]
                        },
                        {
                            'keyframe_selector': 100,
                            'properties': [
                                {
                                    'property_name': 'top',
                                    'property_value': {
                                        'type': 'length',
                                        'value': 200,
                                        'unit': 'px'
                                    }
                                }
                            ]
                        }
                    ]
                }
            )
        ]

        for rule, expected_parsed_rule in rule_data:
            parsed_rule = parse_rule(rule)
            print(parsed_rule)
            self.assertTrue(parsed_rule, expected_parsed_rule)
        self.assertTrue(False)
