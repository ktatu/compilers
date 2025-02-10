from dataclasses import dataclass
import compiler.ast as ast
from compiler.types import *


@dataclass
class SymTab:
    locals: dict[str, Type]
    parent: "SymTab" = None


def typecheck(node: ast.Expression, sym_tab: SymTab = None) -> Type:
    current_tab: SymTab = SymTab({}, sym_tab)

    def add_symbol_type(node: ast.VariableDeclaration):
        symbol_type = typecheck(node.initialize, current_tab)
        current_tab.locals[node.name] = symbol_type

    def add_top_level_func_types() -> None:
        for arithmetic_op in ["+", "-", "*", "/", "%"]:
            current_tab.locals[arithmetic_op] = FunType(
                (
                    Int,
                    Int,
                ),
                Int,
            )

        for comparison_op in ["<", "<=", ">", ">="]:
            current_tab.locals[comparison_op] = FunType((Int, Int), Bool)

        current_tab.locals["or"] = FunType((Bool, Bool), Bool)
        current_tab.locals["and"] = FunType((Bool, Bool), Bool)

        """ no support or tests for built-in-functions yet
        current_tab.locals["print_int"] = FunType((Int), Unit)
        current_tab.locals["print_bool"] = FunType((Bool), Unit)
        current_tab.locals["read_int"] = FunType((Int), Unit)
        """

    def get_symbol(symbol: str, tab: SymTab = current_tab) -> Type:
        if symbol in tab.locals.keys():
            return tab.locals[symbol]

        if tab.parent is not None:
            return get_symbol(symbol, tab.parent)

        return None

    if sym_tab is None:
        add_top_level_func_types()

    match node:

        case ast.Literal():
            if isinstance(node.value, bool):
                return Bool
            elif isinstance(node.value, int):
                return Int
            else:
                raise Exception(
                    f"{node.location}. Type check error: unexpected type in literal: {type(node.value)}"
                )

        case ast.VariableDeclaration():
            add_symbol_type(node)
            return Unit

        case ast.Identifier():
            identifier_type = get_symbol(node.name)
            if identifier_type is None:
                raise Exception(
                    f"{node.location}. Type check error: could not find type for symbol {node.name}"
                )

            if isinstance(identifier_type, FunType):
                return identifier_type.return_type
            elif isinstance(identifier_type, BasicType):
                return identifier_type
            else:
                raise Exception(
                    f"{node.location}. Type check error: unsupported type declared as variable, {type(identifier_type)}"
                )

        case ast.Block():
            for expr in node.statements:
                if isinstance(expr, ast.VariableDeclaration):
                    add_symbol_type(expr)
                else:
                    # everything is checked for type errors even though doesnt matter for block evaluation
                    typecheck(expr, current_tab)

            if isinstance(node.result, ast.Literal) and node.result.value is None:
                return Unit
            # node.result is None when the node is an empty block
            elif node.result is None:
                return Unit
            else:
                return typecheck(node.result, current_tab)

        case ast.BinaryOp():
            t1 = typecheck(node.left, current_tab)
            t2 = typecheck(node.right, current_tab)

            func_type: FunType = None

            # separately handling operators where both values should have same type (of any type)
            if node.op in ["=", "==", "!="]:
                if t1 != t2:
                    raise Exception(
                        f"{node.location}. Type check error: two values of binary operation had different types, {t1, t2}"
                    )
                if node.op == "=":
                    return Unit
                return Bool
            else:
                func_type = get_symbol(node.op)

            if func_type is None:
                raise Exception(
                    f"{node.location}. Type check error: unsupported BinaryOp, {node.op}"
                )

            if (t1, t2) != func_type.argument_types:
                raise Exception(
                    f"{node.location}. Type check error: expected BinaryOp argument types {func_type.argument_types}, received {t1, t2}"
                )

            return func_type.return_type

        case ast.Conditional():
            t1 = typecheck(node.cond_if, current_tab)

            if t1 is not Bool:
                raise Exception(
                    f"{node.location}. Type check error: type of if-clause's condition was not boolean, was {type(node.cond_if)}"
                )

            t2 = typecheck(node.then, current_tab)
            t3 = typecheck(node.cond_else, current_tab)

            if t2 != t3:
                raise Exception(
                    f"{node.location}. Type check error: if-clause's then and else had differing types, {t2, t3}"
                )

            return t2
