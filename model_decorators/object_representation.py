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


def represent(obj, attrs=None, pretty=False):

    if attrs is None:
        attrs = [name for name in dir(obj) if not name.startswith("__")]

    def represent_attribute():
        v = getattr(obj, a, None)
        quote = "'" if type(v) is str else ""
        pre = "\n  " if pretty else ""
        return f"{pre}{a}={quote}{v}{quote}"

    result = f"{obj.__class__.__name__}("

    if attrs:
        a = attrs[0]
        result += represent_attribute()
        for a in attrs[1:]:
            blank = "" if pretty else " "
            result += f",{blank}"
            result += represent_attribute()

    result += ")"
    return result


def auto_repr(exclude=None):
    """Adds __repr__() and __str__() based on public properties"""

    if not exclude:
        exclude = list()
    elif type(exclude) is not list:
        exclude = list(exclude)

    def wrap_class(cls):
        property_names = get_names_of_all_properties_for_class(cls, exclude)
        setattr(cls, "__repr__", lambda self: represent(self, property_names))
        setattr(cls, "__str__", lambda self: represent(self, property_names))
        return cls

    return wrap_class
