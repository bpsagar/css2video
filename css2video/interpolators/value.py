import copy

from .interpolators import Interpolators


class ValueTypeMismatch(Exception):
    '''Exception raised when there is mismatch between the two values'''


class FunctionValueArgCountMismatch(Exception):
    '''Exception raised when trying to interpolate function values which don't
    have the same number of arguments'''


class ArrayLengthMismatch(Exception):
    '''Exception raised when trying to interpolate array values which don't
    have the same length'''


def interpolate_value(from_value, to_value, fraction, type='linear'):
    '''Interpolate a value between the given two values
    from_value - initial value
    to_value   - final value
    fraction   - fraction position from the initial value
    type       - type of interpolation function'''

    if from_value.get('type') != to_value.get('type'):
        raise ValueTypeMismatch()

    value_type = from_value.get('type')
    interpolator_fn = Interpolators.get_timing_function(name=type)

    required_value = copy.deepcopy(from_value)

    if value_type in ['number', 'length', 'percentage', 'time']:
        # Interpolate the value
        required_value['value'] = interpolator_fn(
            from_value['value'], to_value['value'], fraction)

    if value_type == 'color':
        # Interpolate RGBA values
        required_value['red'] = interpolator_fn(
            from_value['red'], to_value['red'], fraction)
        required_value['green'] = interpolator_fn(
            from_value['green'], to_value['green'], fraction)
        required_value['blue'] = interpolator_fn(
            from_value['blue'], to_value['blue'], fraction)
        required_value['alpha'] = interpolator_fn(
            from_value['alpha'], to_value['alpha'], fraction)

    if value_type in ['text', 'url']:
        # Text values cannot be interpolated.
        # When the fraction is 1, return the final value
        if fraction == 1:
            required_value['value'] = to_value['value']

    if value_type == 'function':
        # Check the argument count of both the values and interpolate each of
        # the value
        from_args = from_value.get('args', [])
        to_args = to_value.get('args', [])
        if len(from_args) != len(to_args):
            raise FunctionValueArgCountMismatch()
        args = []
        for arg1, arg2 in zip(from_args, to_args):
            args.append(interpolate_value(arg1, arg2, fraction, type))
        required_value['args'] = args

    if value_type == 'array':
        # Check the length of the array and interpolate each of the array items
        from_values = from_value.get('values', [])
        to_values = to_value.get('values', [])
        if len(from_values) != len(to_values):
            raise ArrayLengthMismatch()
        values = []
        for value1, value2 in zip(from_values, to_values):
            values.append(interpolate_value(value1, value2, fraction, type))
        required_value['values'] = values

    return required_value
