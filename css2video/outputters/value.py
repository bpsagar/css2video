
class MissingValueType(Exception):
    '''Exception raised when the type of value is not specified'''
    pass


def output_value(value_dict):
    '''Return the value as a string'''
    type = value_dict.get('type')

    if type is None:
        raise MissingValueType()
    if type == 'number':
        return '{value}'.format(**value_dict)
    if type == 'length':
        return '{value}{unit}'.format(**value_dict)
    if type == 'percentage':
        return '{value}%'.format(**value_dict)
    if type == 'time':
        return '{value}s'.format(**value_dict)
    if type == 'color':
        return 'rgba({red}, {green}, {blue}, {alpha})'.format(**value_dict)
    if type == 'text':
        return '{value}'.format(**value_dict)
    if type == 'url':
        return '{value}'.format(**value_dict)
    if type == 'function':
        args = ' '.join([output_value(arg) for arg in value_dict['args']])
        return '{name}({args})'.format(name=value_dict['name'], args=args)
    if type == 'array':
        args = ' '.join([output_value(arg) for arg in value_dict['values']])
        return '{args}'.format(args=args)
