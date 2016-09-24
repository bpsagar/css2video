from .base import BaseParser
from .property import Property
import pyparsing as pp


class Style(BaseParser):
    '''Parse a CSS style rule'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse a CSS style rule'''
        selector = pp.Word(pp.alphanums + '#.,*>+~[]=|^$:-() ')
        return (
            selector +
            pp.Suppress(pp.Literal('{')) +
            pp.ZeroOrMore(Property.parser()) +
            pp.Suppress(pp.Literal('}'))
        )

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'style',
            'selector': tokens[0].strip(),
            'properties': tokens[1:]
        }


class KeyframeProperties(BaseParser):
    '''Parse keyframe properties'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse keyframe properties'''
        keyframe_selector = (
            (
                pp.Word(pp.nums + '.') +
                pp.Suppress(pp.Literal('%')).leaveWhitespace()
            ) |
            pp.Literal('from') |
            pp.Literal('to')
        )
        return (
            keyframe_selector +
            pp.Suppress(pp.Literal('{')) +
            pp.ZeroOrMore(Property.parser()) +
            pp.Suppress(pp.Literal('}'))
        )

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        if tokens[0] == 'from':
            tokens[0] = '0'
        elif tokens[0] == 'to':
            tokens[0] = '100'
        return {
            'keyframe_selector': float(tokens[0]),
            'properties': tokens[1:]
        }


class Keyframes(BaseParser):
    '''Parse a CSS keyframe rule'''

    @classmethod
    def grammar(cls):
        '''Grammar to parse a CSS keyframe rule'''
        name = pp.Word(pp.alphanums + '_-')
        return (
            pp.Suppress(pp.Literal('@keyframes')) +
            name +
            pp.Suppress(pp.Literal('{')) +
            pp.ZeroOrMore(KeyframeProperties.parser()) +
            pp.Suppress(pp.Literal('}'))
        )

    @classmethod
    def parse_action(cls, tokens):
        '''Returns a dictionary from the parsed tokens'''
        return {
            'type': 'keyframes',
            'name': tokens[0],
            'keyframes': tokens[1:]
        }


class Rule(object):
    '''Parse any CSS rule'''

    @classmethod
    def parser(cls):
        '''Grammar to parse any CSS rule'''
        return (
            Style.parser() ^
            Keyframes.parser()
        )
