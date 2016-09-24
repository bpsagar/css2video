import logging

# Cubic bezier function
_cubic_bezier = lambda t, v0, v1, v2, v3: ((1-t)**3) * v0 + 3 * ((1-t)**2) * t * v1 + 3 * (1-t) * (t**2) * v2 + (t**3)*v3


def bezier_interpolate(x1, y1, x2, y2, x, iterations=64):
    assert(x1 >= 0 and x2 >= 0)
    assert(x1 <= 1 and x2 <= 1)

    # search for x
    t = 0.5
    r = 0.5
    while iterations > 0:
        iterations -= 1

        v = _cubic_bezier(t, 0, x1, x2, 1)
        if v == x:
            break
        elif v < x:
            t += r
        else:
            t -= r
        r = r / 2
    logging.debug("Bezier interpolation")
    logging.debug(str((x1, x2, y1, y2, x)))
    logging.debug(str(32 - iterations) + " iteration(s)")
    return _cubic_bezier(t, 0, y1, y2, 1)


res = bezier_interpolate(0.4, 0.2, 0.6, 0.8, 0.5)


class Interpolators:
    '''Standard interpolators'''
    LINEAR = lambda v1, v2, f: v1 * (1-f) + v2 * f
    EASE = lambda v1, v2, f: Interpolators.LINEAR(v1, v2, bezier_interpolate(0.25,0.1,0.25,1,f))
    EASE_IN = lambda v1, v2, f: Interpolators.LINEAR(v1, v2, bezier_interpolate(0.42,0,1,1,f))
    EASE_OUT = lambda v1, v2, f: Interpolators.LINEAR(v1, v2, bezier_interpolate(0,0,0.58,1,f))
    EASE_IN_OUT = lambda v1, v2, f: Interpolators.LINEAR(v1, v2, bezier_interpolate(0.42,0,0.58,1,f))

    @staticmethod
    def get_timing_function(name):
        name = name.upper()
        name = name.replace('-', '_')
        return getattr(Interpolators, name)
