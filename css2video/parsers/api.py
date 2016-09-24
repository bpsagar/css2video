from .property import Property
from .value import Value


def parse_value(string):
    '''Parse a value'''
    return Value.parser().parseString(string)[0]


def parse_property(string):
    '''Parse a CSS property'''
    return Property.parser().parseString(string)[0]
