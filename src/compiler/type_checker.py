from dataclasses import dataclass
import compiler.ast as ast
from compiler.types import Int, Type, Bool, Plus


@dataclass
class SymTab:
    locals: dict[str, Type]
    parent: "SymTab" = None


def typecheck(node: ast.Expression, sym_tab: SymTab = None) -> Type:
    current_tab: SymTab = SymTab({}, sym_tab)

    def add_symbol(node: ast.VariableDeclaration):
        value = typecheck(node.initialize, current_tab)
        current_tab.locals[node.name] = value

    def add_top_level_symbols() -> None:
        current_tab.locals["+"] = Plus
        current_tab.locals["-"] = lambda x, y: x - y
        current_tab.locals["<"] = lambda x, y: x < y

    def get_top_level_symbol(symbol: str) -> Type:
        tab: SymTab = current_tab

        while tab.parent is not None:
            tab = tab.parent

        return tab.locals[symbol]

    match node:

        case ast.Literal():
            if isinstance(node.value, bool):
                return Bool
            elif isinstance(node.value, int):
                return Int
            else:
                raise Exception(
                    f"{node.location}: unexpected type in literal: {type(node.value)}"
                )

        case ast.BinaryOp():
            t1 = typecheck(node.left)
            t2 = typecheck(node.right)
            if node.op == "+":
                if t1 is not Int or t2 is not Int:
                    raise Exception(
                        f"{node.location}: operation + with types {type(t1)}, {type(t2)}"
                    )
                return Int
            else:
                raise Exception(
                    f"{node.location}: {node.op} is an unsupported operation in typechecker"
                )

        case ast.Conditional():
            t1 = typecheck(node.cond_if)
            if t1 is not Bool:
                raise Exception
            t2 = typecheck(node.then)
            t3 = typecheck(node.cond_else)
            if t2 != t3:
                raise Exception
            return t2
