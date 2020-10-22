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
from typing import GenericMeta, List
from model_decorators.argument_validation.arg_inspection import is_default_defined, get_default_value


def verify_required_args_present(args, kwargs, argspec, arg_list):
    """Verifies that all required arguments (specified by `args` and `kwargs`) are present in a function call, where
    `argspec` is the signature of the called function and `arg_list` the actual arguments of the call."""

    for arg in arg_list:

        if arg in kwargs and kwargs[arg] is not None:
            continue

        index = argspec.args.index(arg)
        if is_default_defined(index, argspec) and get_default_value(index, argspec) not in [None, ""]:
            continue

        if index >= len(args):
            raise ValueError(f"{arg} is required")

        value = args[index]
        if value is not None and value != [None]:
            continue

        raise ValueError(f"{arg} is required")


def verify_call_args_have_expected_types(args, kwargs, argspec):
    """Verifies that all arguments in the call have types that comply to the type annotations in the called
    function/method. The contents of generic lists will also be verified. Returns `None` in case of success,
    raises TypeError in case of failure."""

    for i in range(len(args)):
        arg_name = argspec.args[i]
        type_annotation = argspec.annotations.get(arg_name)
        if not type_annotation:
            continue
        verify_arg_type_is_expected_subclass(args[i], arg_name, type_annotation)

    for key in kwargs:
        type_annotation = argspec.annotations.get(key)
        if not type_annotation:
            continue
        verify_arg_type_is_expected_subclass(kwargs[key], key, type_annotation)


def verify_arg_type_is_expected_subclass(item, arg_name, expected_type):
    """Verifies that the type of `item` is either the expected type or a subclass of it. In case that the expected
    type is a generic list, all elements in the list are checked for the correct type/subclass. `arg_name` is for
    error messaging and identifies the argument that didn't satisfy the type constraint."""

    type_class = expected_type.__class__
    if type_class is GenericMeta:
        __verify_collection_contents(arg_name, expected_type, item)
        return

    actual_type = type(item)
    msg_start = ""

    if type_class is tuple:
        expected_type, msg_start = __unpack_tuple(expected_type)

    if not issubclass(actual_type, expected_type):
        raise TypeError(f"expected {msg_start}'{arg_name}' to be subclass of '{expected_type.__name__}' "
                        f"but actually was type '{actual_type.__name__}'")


def __unpack_tuple(expected_type):
    """Just return the first item in the tuple. Raises error if tuple has more than one items."""
    if len(expected_type) > 1:
        raise RuntimeError("This operation is not fit to deal with this case which results in undefined behavior."
                           "This is a bug that happens because the dev thought it actually wouldn't. Sorry.")
    expected_type = expected_type[0]
    return expected_type, "items in "


def __verify_collection_contents(arg_name, expected_type, item):
    """Goes through collection and checks whether all elements are subclass of the expected type. Raises error if
    item is not iterable."""
    if expected_type.__origin__ is List and item is not None:
        expected_items_type = expected_type.__args__
        for i in item:
            verify_arg_type_is_expected_subclass(i, arg_name, expected_items_type)
