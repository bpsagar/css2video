from .property import output_property


class MissingRuleType(Exception):
    '''Exception raised when the type of rule is not specified'''
    pass


def _output_keyframe_properties(keyframe_dict):
    '''Returns the keyframe properties'''
    properties = '\n\t'.join(
        [output_property(p) for p in keyframe_dict.get('properties', [])])
    return (
        '\t%d%% {\n'
        '\t\t%s\n'
        '\t}'
    ) % (keyframe_dict['keyframe_selector'], properties)


def output_rule(rule_dict):
    '''Returns the rule as a string'''
    type = rule_dict.get('type')

    if type is None:
        raise MissingRuleType()
    if type == 'style':
        properties = '\n\t'.join(
            [output_property(p) for p in rule_dict.get('properties', [])])
        return (
            '%s {\n'
            '\t%s\n'
            '}'
        ) % (rule_dict['selector'], properties)
    if type == 'keyframes':
        keyframe_properties = '\n'.join([
            _output_keyframe_properties(p)
            for p in rule_dict.get('keyframes', [])
        ])
        return (
            '@keyframes %s {\n'
            '%s\n'
            '}'
        ) % (rule_dict['name'], keyframe_properties)
