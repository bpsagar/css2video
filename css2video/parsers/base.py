
class BaseParser(object):
    """
    A base class for all the parsers

    Methods
    -------
    grammar :
        method to be overrridden by inheriting class which defines the grammar
    parse_action :
        method to be overrridden by inheriting class which defines the parse
        action for the matched token
    parser :
        returns a parser by setting the parse action to the grammar
    parse :
        method to parse a string into a dictionary using the grammar and parse
        action
    """

    @classmethod
    def grammar(cls):
        """This method is overridden by the class which inherits the
        BaseParser. The method should return a grammar"""
        raise NotImplemented()

    @classmethod
    def parse_action(cls):
        """This method is overridden by the class which inherits the
        BaseParser. The method should create a dictionary from the parsed
        tokens"""
        raise NotImplemented()

    @classmethod
    def parser(cls):
        """Returns the grammar with parse action set so that once the result is
        parsed, the output is available as a dictionary"""
        return cls.grammar().setParseAction(cls.parse_action)

    @classmethod
    def parse(cls, string):
        """
        Parse a given string using the grammar and parse action and returns
        a dictionary

        Parameters
        ----------
        string : str
            string to be parsed

        Returns
        -------
        dict :
            dictionary after parsing the string
        """
        return cls.parser().parseString(string, parseAll=True)[0]
