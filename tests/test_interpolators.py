import unittest

from css2video.interpolators import interpolate_value
from .utils import isEqual


class TestInterpolators(unittest.TestCase):
    '''Interpolators tests'''

    def test_value(self):
        data = [
            (
                {'type': 'number', 'value': 100},
                {'type': 'number', 'value': 0},
                0.5,
                'linear',
                {'type': 'number', 'value': 50},
            ),
            (
                {
                    'type': 'color', 'red': 0, 'green': 50, 'blue': 200,
                    'alpha': 1
                },
                {
                    'type': 'color', 'red': 0, 'green': 150, 'blue': 0,
                    'alpha': 0.5
                },
                0.5,
                'linear',
                {
                    'type': 'color', 'red': 0, 'green': 100, 'blue': 100,
                    'alpha': 0.75
                },
            )
        ]
        for v1, v2, f, t, expected_value in data:
            v = interpolate_value(v1, v2, f, t)
            self.assertTrue(isEqual(v, expected_value))
