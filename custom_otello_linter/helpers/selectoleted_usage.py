import ast


def get_selectoleted_local_names(import_from_nodes: list[ast.ImportFrom]) -> set[str]:
    """
    Локальные имена символа `selectoleted` из любого `from … import selectoleted [as alias]`.
    Путь модуля не проверяем — только имя импорта.
    """
    names: set[str] = set()
    for node in import_from_nodes:
        for alias in node.names:
            if alias.name == 'selectoleted':
                names.add(alias.asname or 'selectoleted')
    return names


def is_selectoleted_call(func: ast.AST, import_from_nodes: list[ast.ImportFrom]) -> bool:
    """
    Вызов `selectoleted(...)` (или алиаса) в правой части присваивания,
    если в файле импортирован символ selectoleted (из любого модуля).
    """
    if isinstance(func, ast.Name):
        return func.id in get_selectoleted_local_names(import_from_nodes)
    return False


def is_selectoleted_decorator(decorator: ast.AST, import_from_nodes: list[ast.ImportFrom]) -> bool:
    """
    Декоратор `@selectoleted` / `@alias` / `@selectoleted(...)` при импорте символа selectoleted.
    """
    if isinstance(decorator, ast.Name):
        return decorator.id in get_selectoleted_local_names(import_from_nodes)

    if isinstance(decorator, ast.Call):
        return is_selectoleted_call(decorator.func, import_from_nodes)

    return False
