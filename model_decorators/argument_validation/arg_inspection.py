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


def get_default_value(argument_index, argspec):
    """Returns the default value that is specified in the given `argspec` for the argument at the given
    `argument_ index`. There is no distinction between defaulting to None and no default specified. In both of these
    cases `None` is returned."""

    if not argspec.defaults:
        return None

    defaultslen = len(argspec.defaults)
    argslen = len(argspec.args)
    no_defaults = argslen - defaultslen
    default_index = argument_index - no_defaults

    if default_index < 0:
        return None

    return argspec.defaults[default_index]


def is_default_defined(index, argspec):
    """Returns `True` if the argument at `ìndex` of `argspec` has a default value. Otherwise returns `False`."""

    arglen = len(argspec.args) if argspec.args else 0
    defaultslen = len(argspec.defaults) if argspec.defaults else 0

    defaults_defined = defaultslen > 0
    all_args_have_defaults = arglen == defaultslen
    index_is_in_defaults_range = index >= arglen - defaultslen

    return defaults_defined and (all_args_have_defaults or index_is_in_defaults_range)
