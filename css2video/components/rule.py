
class StyleRuleComponent(object):
    '''A wrapper for CSS style rule dictionary object'''

    def __init__(self, rule_dict, *args, **kwargs):
        super(StyleRuleComponent, self).__init__(*args, **kwargs)
        self.Dict = rule_dict

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
            properties[key] = self.properties.get(key)
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


class KeyframePropertiesComponent(object):
    '''A wrapper for CSS keyframe properties inside a keyframes rule'''

    def __init__(self, properties_dict, *args, **kwargs):
        super(KeyframePropertiesComponent, self).__init__(*args, **kwargs)
        self.Dict = properties_dict
        self.time_offset = properties_dict['keyframe_selector']

    @property
    def properties(self):
        '''Returns all the properties as a dictionary'''
        return {
            p['property_name']: p['property_value']
            for p in self.Dict.get('properties', [])
        }


class KeyframesRuleComponent(object):
    '''A wrapper for CSS keyframes rule dictionary object'''

    def __init__(self, rule_dict, *args, **kwargs):
        super(KeyframesRuleComponent, self).__init__(*args, **kwargs)
        self.Dict = rule_dict
        self.name = rule_dict.get('name')
        self.keyframe_properties = [
            KeyframePropertiesComponent(k)
            for k in self.Dict.get('keyframes', [])
        ]
        self.keyframe_properties.sort(key=lambda x: x.time_offset)

    def get_properties_set(self, time_offset):
        '''Get previous and next properties for a time_offset'''
        set1 = set2 = None
        for kfp in self.keyframe_properties:
            if kfp.time_offset <= time_offset:
                set1 = kfp

        for kfp in self.keyframe_properties[::-1]:
            if kfp.time_offset >= time_offset:
                set2 = kfp
        return (set1, set2)
