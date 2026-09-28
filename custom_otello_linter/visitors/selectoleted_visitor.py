import ast
from typing import List

from custom_otello_linter.errors import DecoratorSelectoleted
from custom_otello_linter.helpers.selectoleted_usage import (
    is_selectoleted_call,
    is_selectoleted_decorator,
)
from custom_otello_linter.visitors._visitor_with_filename import VisitorWithFilename


class SelectoletedVisitor(VisitorWithFilename):
    import_from_nodes: List[ast.ImportFrom]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.import_from_nodes = []

    def visit_Module(self, node: ast.Module) -> None:
        self.import_from_nodes = [
            item for item in ast.walk(node) if isinstance(item, ast.ImportFrom)
        ]
        self.generic_visit(node)

    def _report_decorators(self, decorator_list: list[ast.expr]) -> None:
        for decorator in decorator_list:
            if is_selectoleted_decorator(decorator, self.import_from_nodes):
                self.errors.append(DecoratorSelectoleted(decorator.lineno, decorator.col_offset))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._report_decorators(node.decorator_list)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._report_decorators(node.decorator_list)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._report_decorators(node.decorator_list)

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Call) and is_selectoleted_call(
            node.value.func,
            self.import_from_nodes,
        ):
            self.errors.append(DecoratorSelectoleted(node.lineno, node.col_offset))
