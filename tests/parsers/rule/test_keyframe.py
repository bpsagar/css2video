import unittest

from css2video.constants import RuleType
from css2video.parsers.rule import (
    Property, KeyframeProperties, KeyframePropertiesParseException,
    Keyframes, KeyframesParseException
)


class TestCase(unittest.TestCase):

    def test_keyframe_properties_parser(self):
        response = KeyframeProperties.parse('from { margin: 10px; }')
        self.assertEqual(response['selector'], 0.)
        self.assertEqual(response['properties'], [
            Property.parse('margin: 10px;')
        ])

        response = KeyframeProperties.parse('to { padding: 0 5px; }')
        self.assertEqual(response['selector'], 100.)
        self.assertEqual(response['properties'], [
            Property.parse('padding: 0 5px;')
        ])

        response = KeyframeProperties.parse('50% { padding: 0 5px; }')
        self.assertEqual(response['selector'], 50.)
        self.assertEqual(response['properties'], [
            Property.parse('padding: 0 5px;')
        ])

        with self.assertRaises(KeyframePropertiesParseException):
            KeyframeProperties.parse('50 % { ; }')

    def test_keyframes_parser(self):
        keyframes = [
            'from { margin-left: 1000px; }',
            '50% { margin-left: 800px; }',
            'to { margin-left: 0; }'
        ]
        response = Keyframes.parse("""
            @keyframes slide-in {{
                {keyframes}
            }}
        """.format(keyframes='\n'.join(keyframes)))
        self.assertEqual(response['type'], RuleType.keyframes)
        self.assertEqual(response['name'], 'slide-in')
        self.assertEqual(response['keyframes'], [
            KeyframeProperties.parse(kf) for kf in keyframes
        ])

        with self.assertRaises(KeyframesParseException):
            Keyframes.parse('@keyframes asd { from { ; } }')
