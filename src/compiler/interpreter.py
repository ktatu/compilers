from dataclasses import dataclass
from typing import Any, Callable
import compiler.ast as ast

type Value = int | bool | None


@dataclass
class SymTab:
    locals: dict[str, int | str | bool]
    parent: "SymTab" = None


# mistä tiedetään, millä hierarkisella tasolla kullakin hetkellä ollaan?
def interpret(node: ast.Expression, sym_tab: SymTab = None) -> Value:
    current_tab: SymTab = SymTab({}, sym_tab)

    def add_symbol(node: ast.VariableDeclaration):
        value = interpret(node.initializer, current_tab)
        current_tab.locals[node.name] = value

    def add_top_level_symbols() -> None:
        current_tab.locals["+"] = lambda x, y: x + y
        current_tab.locals["-"] = lambda x, y: x - y
        current_tab.locals["<"] = lambda x, y: x < y

    def get_top_level_operation(symbol: str) -> Callable[..., Any]:
        tab: SymTab = current_tab

        while tab.parent is not None:
            tab = tab.parent

        return tab.locals[symbol]

    if sym_tab is None:
        add_top_level_symbols()

    match node:
        case ast.Literal():
            return node.value

        case ast.VariableDeclaration():
            add_symbol(node)
            return None

        case ast.Identifier():
            table = sym_tab
            identifier = None

            try:
                while node.name not in table.locals.keys():
                    table = sym_tab.parent
                identifier = table.locals[node.name]
            except:
                raise Exception(
                    f"{node.location}: could not find value for identifier {node.name}"
                )

            return identifier

        case ast.Block():
            for expr in node.statements:
                if isinstance(expr, ast.VariableDeclaration):
                    add_symbol(expr)

            if isinstance(node.result, ast.Literal) and node.result.value is None:
                return None
            else:
                # jos on Identifier, niin pitäisi aina löytyä sym_tablesta
                if isinstance(expr, ast.Identifier):
                    print("asd")
                else:
                    return interpret(node.result, current_tab)

        case ast.BinaryOp():
            a: Any = interpret(node.left, current_tab)
            b: Any = interpret(node.right, current_tab)

            operation = get_top_level_operation(node.op)
            return operation(a, b)

        case ast.Conditional():
            if interpret(node.cond_if):
                return interpret(node.then, current_tab)
            else:
                return interpret(node.cond_else, current_tab)
