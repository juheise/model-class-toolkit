from model_decorators.object_representation import represent, auto_repr


def test_represent_object():

    class RepresentMe:
        def __init__(self):
            self.x = "xx"
            self.y = "yy"
            self.z = "zz"

    obj = RepresentMe()
    representation = represent(obj, [name for name in dir(obj) if not name.startswith("__")])
    assert representation == "RepresentMe(x='xx', y='yy', z='zz')"


def test_represent_object_pretty():

    class RepresentMe:
        def __init__(self):
            self.x = "xx"
            self.y = "yy"
            self.z = "zz"

    obj = RepresentMe()
    representation = represent(obj, [name for name in dir(obj) if not name.startswith("__")], pretty=True)
    assert representation == "RepresentMe(\n  x='xx',\n  y='yy',\n  z='zz')"


def test_auto_represent_object():

    @auto_repr()
    class RepresentMe:

        @property
        def x(self):
            return "xx"

        @property
        def y(self):
            return "yy"

        @property
        def z(self):
            return "zz"

    assert repr(RepresentMe()) == "RepresentMe(x='xx', y='yy', z='zz')"


def test_that_with_inheritance_only_topmost_representation_comes_through():

    @auto_repr()
    class Base:

        @property
        def x(self):
            return "xx"

    @auto_repr()
    class RepresentMe(Base):

        @property
        def y(self):
            return "yy"

    assert repr(RepresentMe()) == "RepresentMe(x='xx', y='yy')"


def test_that_representation_is_just_class_name_if_represent_attrs_is_not_specified():

    class RepresentMe:
        def __init__(self):
            self.x = "xx"
            self.y = "yy"
            self.z = "zz"

    obj = RepresentMe()
    representation = represent(obj, [])
    assert representation == "RepresentMe()"
