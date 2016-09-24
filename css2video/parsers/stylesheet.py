from .base import BaseParser
from .rule import Rule
import pyparsing as pp


class StyleSheet(BaseParser):
    '''Parse a stylesheet'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse a style sheet'''
        return pp.ZeroOrMore(Rule.parser())

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'rules': [rule for rule in tokens]
        }
