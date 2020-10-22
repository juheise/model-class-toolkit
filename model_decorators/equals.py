"""Copyright 2020 Julian Heise

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from model_decorators.property_names import get_names_of_all_properties_for_class


def is_object_equal(self, other, *compare_attributes):

    if other is self:
        return True
    if not issubclass(other.__class__, self.__class__):
        return False

    for atr in compare_attributes:
        a = getattr(self, atr)
        b = getattr(other, atr)
        if a != b:
            return False

    return True


def auto_eq(exclude=None):
    """Class decorator that adds an __eq__ method which compares based on public properties."""

    if exclude is None:
        exclude = list()
    elif type(exclude) is not list:
        exclude = list(exclude)

    def wrap(cls):
        property_names = get_names_of_all_properties_for_class(cls, exclude)
        setattr(cls, "__eq__", lambda self, other: is_object_equal(self, other, *property_names))
        return cls

    return wrap
