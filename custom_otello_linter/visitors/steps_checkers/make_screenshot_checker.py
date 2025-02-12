from typing import List

from flake8_plugin_utils import Error

from custom_otello_linter.abstract_checkers import StepsChecker
from custom_otello_linter.errors import MultipleScreenshotsError
from custom_otello_linter.helpers.find_make_screenshot_calls import (
    find_make_screenshot_calls
)
from custom_otello_linter.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_steps_checker
class MakeScreenshotChecker(StepsChecker):

    def check_steps(self, context: Context, config) -> List[Error]:
        errors = []

        # Проверяем каждый шаг в сценарии
        for step in context.steps:
            if (
                    step.name.startswith('then')
                    or step.name.startswith('and')
                    or step.name.startswith('but')
            ):
                screenshot_calls = find_make_screenshot_calls(step.body)

                # Если вызовов функции больше одного, добавляем ошибку
                if len(screenshot_calls) > 1:
                    errors.append(MultipleScreenshotsError(
                        lineno=screenshot_calls[1].lineno,
                        col_offset=screenshot_calls[1].col_offset,
                        step_name=step.name))
                    # Прерываем проверку текущего шага после обнаружения ошибки
                    break

        # Возвращаем собранные ошибки после завершения всех шагов

        return errors
