from .base import BaseParser
from .value import Value
import pyparsing as pp


class Property(BaseParser):
    '''Parse a CSS property'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse a CSS property'''
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
        '''Returns a dictionary from the parsed tokens'''
        return {
            'property_name': tokens[0],
            'property_value': tokens[1]
        }
