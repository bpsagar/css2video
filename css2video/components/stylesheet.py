import copy

from .rule import KeyframesRuleComponent
from .rule import StyleRuleComponent


class StyleSheetComponent(object):
    '''A wrapper from stylesheet dictionary object'''

    def __init__(self, stylesheet_dict, *args, **kwargs):
        super(StyleSheetComponent, self).__init__(*args, **kwargs)
        self.Dict = stylesheet_dict
        style_rules = filter(
            lambda x: x['type'] == 'style', self.Dict.get('rules', []))
        self.style_rules = [StyleRuleComponent(rule) for rule in style_rules]
        keyframes_rules = filter(
            lambda x: x['type'] == 'keyframes', self.Dict.get('rules', []))
        self.keyframes_rules = [
            KeyframesRuleComponent(rule) for rule in keyframes_rules]

    def animation_names(self):
        '''Returns a list of animation names'''
        return [rule.name for rule in self.keyframes_rules]

    def get_keyframes_rule(self, name):
        '''Returns the keyframes rule with this name'''
        for keyframes_rule in self.keyframes_rules:
            if name == keyframes_rule.name:
                return keyframes_rule

    def duplicate(self):
        '''Returns a duplicate copy of the component'''
        return StyleSheetComponent(copy.deepcopy(self.Dict))
