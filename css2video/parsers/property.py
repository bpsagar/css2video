import pyparsing as pp

from .base import BaseParser
from .value import Value


class PropertyParseException(Exception):
    """Raised when there is an exception while parsing a property"""
    pass


class Property(BaseParser):
    """Parse a CSS property"""

    ParseException = PropertyParseException

    @classmethod
    def grammar(cls):
        """Grammar to parse a CSS property"""
        name = pp.Word(pp.alphas + '-')
        value = Value.parser()
        return (
            name +
            pp.Suppress(pp.Literal(':')) +
            value +
            pp.Suppress(pp.Literal(";"))
        )

    @classmethod
    def parse_action(cls, tokens):
        """Returns a dictionary from the parsed tokens"""
        return {
            'property_name': tokens[0].lower(),  # Normalize the name
            'property_value': tokens[1]
        }
