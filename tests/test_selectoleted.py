from flake8_plugin_utils import assert_error, assert_not_error

from custom_otello_linter.errors import DecoratorSelectoleted
from custom_otello_linter.visitors.selectoleted_visitor import SelectoletedVisitor


def test_selectoleted_decorator_on_class():
    code = """
    from tools.utils.test_selector.selectoleted import selectoleted

    @selectoleted
    class Scenario:
        pass
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_assign():
    code = """
    from tools.utils.test_selector.selectoleted import selectoleted

    MySchema = selectoleted(schema.dict({}))
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_without_import_not_flagged():
    code = """
    @selectoleted
    class Scenario:
        pass
    """
    assert_not_error(SelectoletedVisitor, code)


def test_selectoleted_decorator_with_call():
    code = """
    from tools.utils.test_selector.selectoleted import selectoleted

    @selectoleted()
    class Scenario:
        pass
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_decorator_on_function():
    code = """
    from tools.utils.test_selector.selectoleted import selectoleted

    @selectoleted
    def opened_page():
        pass
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_decorator_on_async_function():
    code = """
    from tools.utils.test_selector.selectoleted import selectoleted

    @selectoleted
    async def opened_page():
        pass
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_import_as_alias():
    code = """
    from tools.utils.test_selector.selectoleted import selectoleted as sl

    @sl
    class Scenario:
        pass
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_import_path_does_not_matter():
    code = """
    from moved.pkg.selectoleted import selectoleted

    @selectoleted
    class Scenario:
        pass
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_decorator_commented():
    code = """
    from other_package.helpers import selectoleted

    #@selectoleted
    class Scenario:
        pass
    """
    assert_not_error(SelectoletedVisitor, code)


def test_selectoleted_decorator_on_method_in_class():
    code = """
    from tools.utils.test_selector.selectoleted import selectoleted

    class Scenario:
        @selectoleted
        async def when_open_page(self):
            pass
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_assign_in_class_body():
    code = """
    from tools.utils.test_selector.selectoleted import selectoleted

    class SomePage:
        locator = selectoleted('[data-test="x"]')
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)


def test_selectoleted_decorator_before_import_at_bottom():
    code = """
    @selectoleted
    class Scenario:
        pass

    from tools.utils.test_selector.selectoleted import selectoleted
    """
    assert_error(SelectoletedVisitor, code, DecoratorSelectoleted)
