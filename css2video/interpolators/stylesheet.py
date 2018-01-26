from ..components import StyleSheetComponent
from .value import interpolate_value


class MissingProperty(Exception):
    '''Exception raised when a property value is missing while interpolating
    values'''
    pass


class StyleSheetInterpolator(object):
    '''Generate stylesheet dictionary object'''

    def __init__(self, stylesheet_dict, *args, **kwargs):
        super(StyleSheetInterpolator, self).__init__(*args, **kwargs)
        self.stylesheet = StyleSheetComponent.from_dict(Dict=stylesheet_dict)

    def get_time_offset(self, animation_properties, time):
        '''Returns the time offset in percentage for the set of provided
        animation properties at the given time. Return None if the time is not
        within the animation duration'''
        delay = animation_properties['animation-delay']
        duration = animation_properties['animation-duration']
        iteration_count = animation_properties['animation-iteration-count']
        animation_start = delay
        animation_end = delay + (duration * iteration_count)

        if time < animation_start or time > animation_end:
            return None

        time -= delay
        time_offset = time % duration
        return (time_offset * 100) / duration

    def generate(self, time):
        '''Returns a stylesheet dictionary object for the given time'''
        stylesheet = self.stylesheet.duplicate()

        for rule in stylesheet.style_rules:
            animation_properties = rule.animation_properties()
            animation_name = animation_properties.get('animation-name')
            if not animation_name:
                continue

            time_offset = self.get_time_offset(animation_properties, time)
            if time_offset is None:
                continue

            keyframes_rule = stylesheet.get_keyframes_rule(animation_name)
            kfp1, kfp2 = keyframes_rule.get_property_sets(
                time_offset=time_offset)

            if kfp2.time_offset == kfp1.time_offset:
                fraction = 0
            else:
                fraction = (
                    (time_offset - kfp1.time_offset) /
                    (kfp2.time_offset - kfp1.time_offset)
                )

            for pname1, value1 in kfp1.properties.items():
                if pname1 not in kfp2.properties:
                    raise MissingProperty('Missing property %s' % pname1)
                value2 = kfp2.properties[pname1]
                value = interpolate_value(
                    from_value=value1, to_value=value2, fraction=fraction,
                    type=animation_properties['animation-timing-function'])
                rule.add_property(name=pname1, value=value)
        return stylesheet


def interpolate_stylesheet(stylesheet_dict, time):
    """Interpolates the animation property value based on the given time and
    returns the resulting stylesheet as a dictionary"""
    generator = StyleSheetInterpolator(stylesheet_dict=stylesheet_dict)
    return generator.generate(time=time).to_dict()
