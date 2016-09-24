from .value import Value


def parse_value(string):
    '''Parse a value'''
    return Value.parser().parseString(string)[0]
