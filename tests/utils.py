
def isEqual(value1, value2):
    '''Compare any two values and returns true if they are equal'''
    if isinstance(value1, list) and isinstance(value2, list):
        is_equal = True
        for v1, v2 in zip(value1, value2):
            is_equal = is_equal and isEqual(v1, v2)
            if not is_equal:
                break
        return is_equal

    if isinstance(value1, dict) and isinstance(value2, dict):
        is_equal = len(value1.keys()) == len(value2.keys())
        for key1 in value1:
            is_equal = is_equal and (key1 in value2)
            if not is_equal:
                break
            is_equal = is_equal and isEqual(value1[key1], value2[key1])
            if not is_equal:
                break
        return is_equal
    return value1 == value2
