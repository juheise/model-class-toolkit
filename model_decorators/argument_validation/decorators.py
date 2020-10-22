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

import inspect
from functools import wraps

from model_decorators.argument_validation.verifications import verify_required_args_present, \
    verify_call_args_have_expected_types


def required_args(*arg_list):
    """Decorator that enforces the arguments specified by `*arg_list` are present in a call. If any of the required
    args is missing, `None` or in any way empty (e.g.: `[]`, `{}`, `""`, etc.), a `ValueError` is raised."""

    def wrapper(fn):

        argspec = inspect.getfullargspec(fn)
        __assert_all_arguments_in_target_function(argspec, fn)

        @wraps(fn)
        def wrapped(*args, **kwargs):
            verify_required_args_present(args, kwargs, argspec, arg_list)
            return fn(*args, **kwargs)

        __update_wrapper_signature(fn, wrapped)
        return wrapped

    def __assert_all_arguments_in_target_function(argspec, fn):
        for arg in arg_list:
            if not arg in argspec.args:
                raise KeyError(f"expected argument '{arg}' not in signature of {fn.__name__}")

    return wrapper


def __update_wrapper_signature(fn, wrapped):
    """Replaces the signature of `ẁrapped` with the signature of `fn`."""

    sig = inspect.signature(fn)

    if inspect.ismethod(fn):
        parameters = tuple(sig.parameters.values())[1:]
    else:
        parameters = tuple(sig.parameters.values())

    sig = sig.replace(parameters=parameters)
    wrapped.__signature__ = sig


def enforce_arg_types(fn):
    """Decorator that raises an error if any of the arguments given in the call are not subclasses of the types
    specified via type annotations. Does not verify `None`."""

    argspec = inspect.getfullargspec(fn)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_call_args_have_expected_types(args, kwargs, argspec)
        return fn(*args, **kwargs)

    __update_wrapper_signature(fn, wrapper)
    return wrapper
