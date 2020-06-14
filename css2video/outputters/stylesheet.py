from .rule import output_rule


def output_stylesheet(stylesheet_dict):
    '''Returns the stylesheet as a string'''
    return '\n'.join(
        [output_rule(rule) for rule in stylesheet_dict.get('rules', []) if rule['type'] == 'style'])
