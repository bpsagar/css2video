import unittest

from css2video.constants import ValueType
from css2video.parsers.value import Function, FunctionParseException


class TestCase(unittest.TestCase):

    def test_parser(self):
        response = Function.parse('url("background.png")')
        self.assertEqual(
            response,
            dict(type=ValueType.function, name='url', args=[
                dict(type=ValueType.url, value='"background.png"')
            ])
        )

        response = Function.parse('translate(0 20px)')
        self.assertEqual(
            response,
            dict(type=ValueType.function, name='translate', args=[
                dict(type=ValueType.number, value=0.),
                dict(type=ValueType.length, value=20., unit='px')
            ])
        )

        with self.assertRaises(FunctionParseException):
            Function.parse('hello')
