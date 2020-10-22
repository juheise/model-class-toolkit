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
from model_decorators.equals import auto_eq
from model_decorators.object_representation import auto_repr


def model_class(exclude_eq=None, exclude_repr=None, exclude=None):

    if not exclude_eq:
        exclude_eq = list()
    if not exclude_repr:
        exclude_repr = list()

    if exclude:
        exclude_eq.extend(exclude)
        exclude_repr.extend(exclude)

    def wrap(cls):

        auto_eq_wrapper = auto_eq(exclude=exclude_eq)
        auto_eq_wrapper(cls)

        auto_repr_wrapper = auto_repr(exclude=exclude_repr)
        auto_repr_wrapper(cls)

        return cls

    return wrap
