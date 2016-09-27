from .base import BaseComponent
from .rule import KeyframesRuleComponent
from .rule import StyleRuleComponent


class StyleSheetComponent(BaseComponent):
    """A wrapper from stylesheet dictionary object"""

    def __init__(self, *args, **kwargs):
        super(StyleSheetComponent, self).__init__(*args, **kwargs)

    @property
    def style_rules(self):
        """Returns the style components"""
        style_rules = filter(
            lambda x: x['type'] == 'style', self.Dict.get('rules', []))
        return [
            StyleRuleComponent.from_dict(Dict=rule) for rule in style_rules
        ]

    @property
    def keyframes_rules(self):
        keyframes_rules = filter(
            lambda x: x['type'] == 'keyframes', self.Dict.get('rules', []))
        return [
            KeyframesRuleComponent.from_dict(Dict=rule)
            for rule in keyframes_rules
        ]

    def animation_names(self):
        """Returns a list of animation names"""
        return [rule.name for rule in self.keyframes_rules]

    def get_keyframes_rule(self, name):
        """Returns the keyframes rule with this name
        Args:
            - name: name of the animation
        """
        for keyframes_rule in self.keyframes_rules:
            if name == keyframes_rule.name:
                return keyframes_rule
