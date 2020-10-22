from model_decorators.equals import auto_eq


def test_auto_eq_simple():

    @auto_eq()
    class A:

        def __init__(self, value):
            self.value = value

        @property
        def a(self):
            return self.value

    assert A(1) == A(1)
    assert A(1) != A(2)


def test_auto_eq_multiple_properties():

    @auto_eq()
    class A:

        def __init__(self, a, b, c):
            self.__a = a
            self.__b = b
            self.__c = c

        @property
        def a(self):
            return self.__a

        @property
        def b(self):
            return self.__b

        @property
        def c(self):
            return self.__c

    assert A(1, 2, 3) == A(1, 2, 3)
    assert A(1, 2, 3) != A(3, 2, 1)
    assert A(1, 2, 3) != A(1, 3, 2)
    assert A(1, 2, 3) != A(2, 1, 3)
    assert A(1, 2, 3) != A(2, 3, 1)


def test_auto_eq_ignore():

    @auto_eq(exclude=["b"])
    class A:

        def __init__(self, a, b):
            self.__a = a
            self.__b = b

        @property
        def a(self):
            return self.__a

        @property
        def b(self):
            return self.__b

        def __repr__(self):
            return f"A(a={self.a}, b={self.b})"

    assert A(1, 2) == A(1, 2)
    assert A(1, 2) == A(1, 3)
    assert A(1, 2) != A(3, 2)


def test_that_auto_eq_can_deal_with_inheritance():

    @auto_eq()
    class A:

        def __init__(self, a):
            self.__a = a

        @property
        def a(self):
            return self.__a

    @auto_eq()
    class B(A):

        def __init__(self, a, b):
            super().__init__(a)
            self.__b = b

        @property
        def b(self):
            return self.__b

    assert B(1, 2) == B(1, 2)
    assert B(2, 1) != B(1, 2)
