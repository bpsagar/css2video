
class NotImplementedError(Exception):
    '''Exception class for not implemented parts of the code'''
    pass


class BaseParser(object):
    '''A base class for all the parser'''

    @classmethod
    def grammar(cls):
        '''This method is overridden by the class which inherits the
        BaseParser. The method should return a grammar'''
        raise NotImplementedError()

    @classmethod
    def parse_action(cls):
        '''This method is overridden by the class which inherits the
        BaseParser. The method should create a dictionary from the parsed
        tokens'''
        raise NotImplementedError()

    @classmethod
    def parser(cls):
        '''Returns the grammar with parse action set so that once the result is
        parsed, the output is available as a dictionary'''
        return cls.grammar().setParseAction(cls.parse_action)
