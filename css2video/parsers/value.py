import pyparsing as pp

from css2video.constants import ValueType
from .base import BaseParser


class NumberParseException(Exception):
    """Raised when there is an exception while parsing a number"""
    pass


class Number(BaseParser):
    """Parser to parse a number"""

    ParseException = NumberParseException

    @classmethod
    def grammar(cls):
        """Returns the grammar to parse a number that may have a sign and a
        decimal point"""
        sign = pp.Word('+-', exact=1)
        digits = pp.Word(pp.nums)
        decimal = pp.Combine(pp.Word('.', exact=1) + digits)
        return pp.Combine(pp.Optional(sign) + digits + pp.Optional(decimal))

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        return {
            'type': ValueType.number,
            'value': float(tokens[0])
        }


class LengthParseException(Exception):
    """Raised when there is an execption while parsing a length"""
    pass


class Length(BaseParser):
    """Parse a length value that has a unit attached along with the number"""

    ParseException = LengthParseException

    UNITS = ['em', 'ex', 'px', 'cm', 'mm', 'in', 'pt', 'pc', 'deg']

    @classmethod
    def grammar(cls):
        """Grammar to parse the length value"""
        number = Number.grammar()
        units = pp.CaselessLiteral(cls.UNITS[0])
        for unit in cls.UNITS[1:]:
            units |= pp.Literal(unit)
        return number + units.leaveWhitespace()

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        return {
            'type': ValueType.length,
            'value': float(tokens[0]),
            'unit': tokens[1].lower()  # normalizing the units
        }


class PercentageParseException(Exception):
    """Raised when there is an exception while parsing a percentage value"""
    pass


class Percentage(BaseParser):
    """Parse a percentage value"""

    ParseException = PercentageParseException

    @classmethod
    def grammar(cls):
        """Grammar to parse the percentage value"""
        number = Number.grammar()
        percentage = pp.Literal('%').leaveWhitespace()
        return number + percentage

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        return {
            'type': ValueType.percentage,
            'value': float(tokens[0]),
        }


class TimeParseException(Exception):
    """Raised when there is an execption while parsing a time value"""
    pass


class Time(BaseParser):
    """Parse a time value which is in seconds"""

    ParseException = TimeParseException

    @classmethod
    def grammar(cls):
        """Grammar to parse a time value"""
        number = Number.grammar()
        seconds = pp.CaselessLiteral('s').leaveWhitespace()
        return number + seconds

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        return {
            'type': ValueType.time,
            'value': float(tokens[0])
        }


class ColorParseException(Exception):
    """Raised when there is an exception while parsing a color value"""
    pass


class Color(BaseParser):
    """Parse a color value. It can be hex, RGB or RGBA"""

    ParseException = ColorParseException

    HEX_CHARS = '0123456789ABCDEFabcdef'

    @classmethod
    def grammar(cls):
        """Grammar to parse a color value"""
        hex3 = (
            pp.Suppress(pp.Literal('#')) +
            pp.Word(cls.HEX_CHARS, exact=3).leaveWhitespace()
        )
        hex6 = (
            pp.Suppress(pp.Literal('#')) +
            pp.Word(cls.HEX_CHARS, exact=6).leaveWhitespace()
        )
        rgb = (
            pp.Suppress(pp.CaselessLiteral('rgb(')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(')'))
        )
        rgba = (
            pp.Suppress(pp.CaselessLiteral('rgba(')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(',')) +
            Number.grammar() +
            pp.Suppress(pp.Literal(')'))
        )
        return hex6 | hex3 | rgba | rgb

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        alpha = 1
        if len(tokens) == 1:
            red, green, blue = cls.hex_to_rgb(tokens[0])
        elif len(tokens) == 3:
            red, green, blue = map(float, tokens)
        elif len(tokens) == 4:
            red, green, blue, alpha = map(float, tokens)

        return {
            'type': ValueType.color,
            'red': red,
            'green': green,
            'blue': blue,
            'alpha': alpha
        }

    @classmethod
    def hex_to_rgb(cls, hexval):
        """Convert hex value to RGB value"""
        if len(hexval) == 3:
            new_hexval = ''
            for c in hexval:
                new_hexval += c * 2
            hexval = new_hexval
        return [int(hexval[i:i + 2], base=16)for i in range(0, 6, 2)]


class TextParseException(Exception):
    """Raised when there is an exception while parsing a text value"""
    pass


class Text(BaseParser):
    """Parse a text value"""

    ParseException = TextParseException

    @classmethod
    def grammar(cls):
        """Grammar to parse a text value"""
        return pp.Word(pp.alphas + '-')

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        return {
            'type': ValueType.text,
            'value': tokens[0]
        }


class UrlParseException(Exception):
    """Raised when there is an exception while parsing an URL value"""
    pass


class Url(BaseParser):
    """Parse a URL value which is usually a quoted string"""

    ParseException = UrlParseException

    @classmethod
    def grammar(cls):
        """Grammar to parse a URL value"""
        return pp.quotedString

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        return {
            'type': ValueType.url,
            'value': tokens[0]
        }


class FunctionParseException(Exception):
    """Raised when there is an while parsing a function value"""
    pass


class Function(BaseParser):
    """Parse a function value with optional arguments passed"""

    ParseException = FunctionParseException

    @classmethod
    def grammar(cls):
        """Grammar to parse a function value"""
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
        """Returns a dictionary from the parsed tokens"""
        return {
            'type': ValueType.function,
            'name': tokens[0],
            'args': tokens[1:]
        }

    @classmethod
    def args_parser(cls):
        """Returns the arguments of the function which can be a Number, Length,
        Percentage, Time, Color, Text or URL"""
        arg_types = [Number, Length, Percentage, Time, Color, Text, Url]
        arg_parser = arg_types[0].parser()
        for arg_type in arg_types[1:]:
            arg_parser ^= arg_type.parser()
        return pp.OneOrMore(arg_parser)


class ArrayParseException(Exception):
    """Raised when there is an exception while parsing an array value"""
    pass


class Array(BaseParser):
    """Parse an array value. The array item values can be of any type"""

    ParseException = ArrayParseException

    @classmethod
    def grammar(cls):
        """Grammar to parse an array value"""
        array_types = [
            Number, Length, Percentage, Time, Color, Text, Url, Function]
        array_parser = array_types[0].parser()
        for array_type in array_types[1:]:
            array_parser ^= array_type.parser()
        return array_parser + pp.OneOrMore(array_parser)

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        return {
            'type': ValueType.array,
            'values': [value for value in tokens]
        }


class Value(object):
    """Parse any CSS property value"""

    @classmethod
    def parser(cls):
        """Grammar to parse any CSS Property value"""
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
