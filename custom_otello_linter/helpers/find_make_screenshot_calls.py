import ast

from custom_otello_linter.helpers.get_full_func_name import get_full_func_name


def find_make_screenshot_calls(step_body):
    """
    Проверяет наличие вызова функции make_screenshot_for_comparison в тесте.
    Возвращает список узлов AST, соответствующих этим вызовам
    """
    make_screenshot_calls = []

    # Проходим через каждый элемент в теле функции (step.body)
    for stmt in step_body:
        # Применяем ast.walk к каждому выражению в теле функции
        for node in ast.walk(stmt):
            if isinstance(node, ast.Call):
                func_name = get_full_func_name(node.func)

                # Проверяем вызов функции make_screenshot_for_comparison
                if func_name.endswith('make_screenshot_for_comparison'):
                    make_screenshot_calls.append(node)

    return make_screenshot_calls
