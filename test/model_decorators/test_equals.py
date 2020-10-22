import pytest

from model_decorators.equals import is_object_equal


class T:
    def __init__(self, a=None, b=None, c=None):
        self.a = a
        self.b = b
        self.c = c

    def __eq__(self, other):
        return is_object_equal(self, other, "a", "b", "c")


class TT:
    def __init__(self, ts):
        self.ts = ts

    def __eq__(self, other):
        return is_object_equal(self, other, "ts")


t = T()


@pytest.mark.parametrize("a, b, expected", [

    (T(1, 2, 3), T(1, 2, 3), True),
    (T(), T(), True),
    (T(1), T(1), True),
    (T(1, 2, 3), T(3, 2, 1), False),
    (T(1, 2, 3), list(), False),
    (t, t, True),

    # cases with list comparison
    (TT([T(1, 2, 3), T(3, 2, 1)]), TT([T(1, 2, 3), T(3, 2, 1)]), True),
    (TT([T(1, 2, 3), T(3, 2, 1)]), TT([T(3, 2, 1), T(1, 2, 3)]), False),
    (TT([T(1, 2, 3), T(3, 2, 1)]), TT([T(1, 2, 3)]), False),
    (TT([T(1, 2, 3), T(3, 2, 1)]), TT([T(1, 2, 3), T(1, 1, 1)]), False),
    (TT([T(1, 2, 3), T(3, 2, 1)]), TT([]), False),
    (TT([]), TT([]), True)
])
def test_is_object_equal(a, b, expected):
    assert (a == b) == expected
