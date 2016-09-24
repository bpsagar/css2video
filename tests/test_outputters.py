import unittest

from css2video.outputters import output_property
from css2video.outputters import output_rule
from css2video.outputters import output_stylesheet
from css2video.outputters import output_value


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
            'rgba(255, 255, 255, 1)': {
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
        for expected_value_string, value_dict in value_data.items():
            value_string = output_value(value_dict)
            self.assertEqual(value_string, expected_value_string)

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
                'box-shadow: 0px 0px 4px rgba(0, 0, 0, 1);',
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
        for expected_property_string, property_dict in property_data:
            property_string = output_property(property_dict)
            self.assertEqual(property_string, expected_property_string)

    def test_rule(self):
        rule_data = [
            (
                (
                    'div {\n'
                    '\tmargin-top: 20px;\n'
                    '}'
                ),
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
                (
                    '@keyframes mymove {\n'
                    '\t0% {\n'
                    '\t\ttop: 0px;\n'
                    '\t}\n'
                    '\t100% {\n'
                    '\t\ttop: 200px;\n'
                    '\t}\n'
                    '}'
                ),
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

        for expected_rule_string, rule_dict in rule_data:
            rule_string = output_rule(rule_dict)
            self.assertEqual(rule_string, expected_rule_string)

    def test_stylesheet(self):
        stylesheet_data = [
            (
                (
                    'div {\n'
                    '\tmargin-top: 20px;\n'
                    '}\n'
                    '@keyframes mymove {\n'
                    '\t0% {\n'
                    '\t\ttop: 0px;\n'
                    '\t}\n'
                    '\t100% {\n'
                    '\t\ttop: 200px;\n'
                    '\t}\n'
                    '}'
                ),
                {
                    'rules': [
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
                        },
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
                    ]
                }
            )
        ]

        for expected_string, stylesheet_dict in stylesheet_data:
            string = output_stylesheet(stylesheet_dict)
            self.assertEqual(string, expected_string)
