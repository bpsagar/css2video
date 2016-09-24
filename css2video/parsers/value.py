from .base import BaseParser
import pyparsing as pp


class Number(BaseParser):
    '''Parse a number value that may have a sign, decimal point'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse the number value'''
        sign = pp.Word('+-', exact=1)
        digits = pp.Word(pp.nums)
        decimal = pp.Combine(pp.Word('.', exact=1) + digits)

        return pp.Combine(pp.Optional(sign) + digits + pp.Optional(decimal))

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'number',
            'value': float(tokens[0])
        }


class Length(BaseParser):
    '''Parse a length value that has a unit attached along with the number'''

    UNITS = ['em', 'ex', 'px', 'cm', 'mm', 'in', 'pt', 'pc', 'deg']

    @classmethod
    def grammar(cls):
        '''Grammar to parse the length value'''
        number = Number.grammar()
        units = pp.Literal(cls.UNITS[0])
        for unit in cls.UNITS[1:]:
            units |= pp.Literal(unit)

        return number + units.leaveWhitespace()

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'length',
            'value': float(tokens[0]),
            'unit': tokens[1]
        }


class Percentage(BaseParser):
    '''Parse a percentage value'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse the percentage value'''
        number = Number.grammar()
        percentage = pp.Literal('%').leaveWhitespace()

        return number + percentage

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'percentage',
            'value': float(tokens[0]),
        }


class Time(BaseParser):
    '''Parse a time value which is in seconds'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse a time value'''
        number = Number.grammar()
        seconds = pp.Literal('s').leaveWhitespace()

        return number + seconds

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'time',
            'value': float(tokens[0])
        }


class Color(BaseParser):
    '''Parse a color value. It can be hex, RGB or RGBA'''

    HEX_CHARS = '0123456789ABCDEFabcdef'

    @classmethod
    def grammar(cls):
        '''Grammar to parse a color value'''
        hex3 = (
            pp.Suppress(pp.Literal('#')) +
            pp.Word(cls.HEX_CHARS, exact=3).leaveWhitespace()
        )
        hex6 = (
            pp.Suppress(pp.Literal('#')) +
            pp.Word(cls.HEX_CHARS, exact=6).leaveWhitespace()
        )
        rgb = (
            pp.Suppress(pp.Literal('rgb(')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(')'))
        )
        rgba = (
            pp.Suppress(pp.Literal('rgba(')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(')'))
        )
        return hex3 | hex6 | rgb | rgba

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        alpha = 1
        if len(tokens) == 1:
            red, green, blue = cls.hex_to_rgb(tokens[0])
        elif len(tokens) == 3:
            red, green, blue = map(float, tokens)
        elif len(tokens) == 4:
            red, green, blue, alpha = map(float, tokens)

        return {
            'type': 'color',
            'red': red,
            'green': green,
            'blue': blue,
            'alpha': alpha
        }

    @classmethod
    def hex_to_rgb(cls, hexval):
        '''Convert hex value to RGB value'''
        if len(hexval) == 3:
            new_hexval = ''
            for c in hexval:
                new_hexval += c * 2
            hexval = new_hexval
        return [int(hexval[i:i + 2], base=16)for i in range(0, 6, 2)]


class Text(BaseParser):
    '''Parse a text value'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse a text value'''
        return pp.Word(pp.alphas + '-')

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'text',
            'value': tokens[0]
        }


class Url(BaseParser):
    '''Parse a URL value which is usually a quoted string'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse a URL value'''
        return pp.quotedString

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'url',
            'value': tokens[0]
        }


class Function(BaseParser):
    '''Parse a function value with optional arguments passed'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse a function value'''
        name = pp.Word(pp.alphas)
        args = cls.args_parser()

        return (
            name +
            pp.Suppress(pp.Literal('(')) +
            args +
            pp.Suppress(pp.Literal(')'))
        )

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'function',
            'name': tokens[0],
            'args': tokens[1:]
        }

    @classmethod
    def args_parser(cls):
        '''Returns the arguments of the function which can be a Number, Length,
        Percentage, Time, Color, Text or URL'''
        arg_types = [Number, Length, Percentage, Time, Color, Text, Url]
        arg_parser = arg_types[0].parser()
        for arg_type in arg_types[1:]:
            arg_parser ^= arg_type.parser()
        return pp.OneOrMore(arg_parser)


class Array(BaseParser):
    '''Parse an array value. The array item values can be of any type'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse an array value'''
        array_types = [
            Number, Length, Percentage, Time, Color, Text, Url, Function]
        array_parser = array_types[0].parser()
        for array_type in array_types[1:]:
            array_parser ^= array_type.parser()
        return array_parser + pp.OneOrMore(array_parser)

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'array',
            'values': [value for value in tokens]
        }


class Value(object):
    '''Parse any CSS property value'''

    @classmethod
    def parser(cls):
        '''Grammar to parse any CSS Property value'''
        return (
            Number.parser() ^
            Length.parser() ^
            Percentage.parser() ^
            Time.parser() ^
            Color.parser() ^
            Text.parser() ^
            Url.parser() ^
            Function.parser() ^
            Array.parser()
        )
