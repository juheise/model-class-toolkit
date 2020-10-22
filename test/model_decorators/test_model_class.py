from model_decorators.model_class import model_class


def test_that_setting_exclude_excludes_autorepr_for_property():

    @model_class(exclude=["x"])
    class M:

        @property
        def x(self):
            return "this should be excluded"

        @property
        def y(self):
            return "this should be included"

    assert repr(M()) == "M(y='this should be included')"
