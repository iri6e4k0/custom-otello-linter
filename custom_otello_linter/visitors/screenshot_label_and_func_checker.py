import ast
from typing import List

from flake8_plugin_utils import Error

from custom_otello_linter.abstract_checkers import StepsChecker
from custom_otello_linter.abstract_checkers.get_full_func_name import (
    get_full_func_name
)
from custom_otello_linter.errors import (
    MissingAllureScreenshotsLabelError,
    MissingMakeScreenshotFuncCallError
)
from custom_otello_linter.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_steps_checker
class ScreenshotsLabelAndFuncChecker(StepsChecker):

    def check_steps(self, context: Context, config) -> List[Error]:
        errors = []

        allure_decorator = self.get_allure_decorator(context.scenario_node)
        has_screenshot_label = False
        has_screenshot_func = False

        # Проверяем, есть ли в списке лейблов SCREENSHOTS
        if allure_decorator:
            allure_tags = self.get_allure_tag_names(allure_decorator)
            has_screenshot_label = "SCREENSHOTS" in allure_tags

        # Проверяем наличие вызова функции make_screenshot_for_comparison
        for step in context.steps:
            for stmt in step.body:
                for node in ast.walk(stmt):
                    if isinstance(node, ast.Call):
                        func_name = get_full_func_name(node.func)
                        if func_name.endswith("make_screenshot_for_comparison"):
                            has_screenshot_func = True
                            break

        # Если в тесте есть лейбл, но нет вызова функции – добавляем ошибку
        if has_screenshot_label and not has_screenshot_func:
            errors.append(MissingMakeScreenshotFuncCallError(
                lineno=context.scenario_node.lineno,
                col_offset=context.scenario_node.col_offset))

        # Если в тесте есть вызов функции, но нет лейбла – добавляем ошибку
        if has_screenshot_func and not has_screenshot_label:
            errors.append(MissingAllureScreenshotsLabelError(
                lineno=allure_decorator.lineno,
                col_offset=allure_decorator.col_offset))

        # Возвращаем собранные ошибки после завершения всех шагов
        return errors
