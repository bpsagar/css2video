from .base import BaseComponent


class StyleRuleComponent(BaseComponent):
    """A wrapper for CSS style rule dictionary object"""

    def __init__(self, *args, **kwargs):
        super(StyleRuleComponent, self).__init__(*args, **kwargs)

    @property
    def properties(self):
        '''Returns all the properties as a dictionary'''
        return {
            p['property_name']: p['property_value']
            for p in self.Dict.get('properties', [])
        }

    def animation_properties(self):
        '''Returns all the animation related properties as a dictionary'''
        properties = {
            'animation-name': '',
            'animation-duration': 0,
            'animation-delay': 0,
            'animation-iteration-count': 1,
            'animation-timing-function': 'ease'
        }
        for key in properties:
            if self.properties.get(key):
                value = self.properties.get(key)
                properties[key] = value.get('value')
        return properties

    def property_list(self):
        '''Returns a list of property names'''
        return [p['property_name'] for p in self.Dict.get('properties', [])]

    def add_property(self, name, value):
        '''Add a new property and value'''
        self.Dict['properties'].append({
            'property_name': name,
            'property_value': value
        })


class KeyframePropertiesComponent(BaseComponent):
    """A wrapper for CSS keyframe properties inside a keyframes rule"""

    def __init__(self, *args, **kwargs):
        super(KeyframePropertiesComponent, self).__init__(*args, **kwargs)

    @property
    def time_offset(self):
        return self.Dict.get('keyframe_selector')

    @property
    def properties(self):
        '''Returns all the properties as a dictionary'''
        return {
            p['property_name']: p['property_value']
            for p in self.Dict.get('properties', [])
        }


class KeyframesRuleComponent(BaseComponent):
    """A wrapper for CSS keyframes rule dictionary object"""

    def __init__(self, *args, **kwargs):
        super(KeyframesRuleComponent, self).__init__(*args, **kwargs)

    @property
    def name(self):
        """Name of animation"""
        return self.Dict.get('name')

    @property
    def keyframe_properties(self):
        """Keyframe properties of the animation"""
        keyframe_properties = [
            KeyframePropertiesComponent(k)
            for k in self.Dict.get('keyframes', [])
        ]
        keyframe_properties.sort(key=lambda x: x.time_offset)
        return keyframe_properties

    def get_property_sets(self, time_offset):
        """For a given time offset, it returns the keyframe properties
        before and after this time offset

        Args:
            - time_offset: time offset in percentage

        Returns:
            (props_1, props_2) where props_1 are properties before
            the time offset and props_2 are properties after the time offset
        """
        set1 = set2 = None
        for kfp in self.keyframe_properties:
            if kfp.time_offset <= time_offset:
                set1 = kfp

        for kfp in self.keyframe_properties[::-1]:
            if kfp.time_offset >= time_offset:
                set2 = kfp
        return (set1, set2)
