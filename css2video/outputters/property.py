from .value import output_value


def output_property(property_dict):
    '''Returns the property as a string'''
    value = output_value(property_dict['property_value'])
    return '{name}: {value};'.format(
        name=property_dict['property_name'], value=value)
