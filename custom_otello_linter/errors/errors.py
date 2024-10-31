from flake8_plugin_utils import Error


class DecoratorVedroParams(Error):
    code = 'OCS101'
    message = 'decorator @vedro.params or params decorator from vedro package should not be presented'


class MultipleScreenshotsError(Error):
    code = 'OCS300'
    message = 'step "{step_name}" make_screenshot_for_comparison is used more than once'
