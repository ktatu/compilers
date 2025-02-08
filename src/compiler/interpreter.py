from dataclasses import dataclass
from typing import Any
import compiler.ast as ast

type Value = int | bool | None


@dataclass
class SymTab:
    locals: dict[str, int | str | bool]
    parent: "SymTab" = None


# mistä tiedetään, millä hierarkisella tasolla kullakin hetkellä ollaan?
def interpret(node: ast.Expression, sym_tab: SymTab = None) -> Value:
    def add_symbol(node: ast.VariableDeclaration):
        value = interpret(node.initialize)

        if sym_tab is not None:
            sym_tab[node.name] = value
        else:
            locals_dict = {node.name: value}
            sym_tab = SymTab(locals_dict)

    match node:
        case ast.Literal():
            return node.value

        # tässä asetetaan sym_tabiin arvo joka määritetään
        # var y = 5; var x = y; pitäisi toimia, y pitää lukea symbol tablesta
        # tässä on kylläkin block
        case ast.VariableDeclaration():
            add_symbol(node)
            return None

        # case { var x = 5; x }, x on result
        # oletetaan, että tämä on ylin taso: ei voida vaan suoraan hypätä resulttiin
        # pitää varmistaa, että VariableDeclaration käsitellään jossain vaiheessa
        # x:n pitää löytyä joko saman tason blockista tai jostakin parent-tablesta
        case ast.Block():
            for expr in node.statements:
                if isinstance(expr, ast.VariableDeclaration):
                    add_symbol(expr)

            if node.result.value is None:
                return None
            else:
                return interpret(node.result, sym_tab)

        case ast.BinaryOp():
            a: Any = interpret(node.left, sym_tab)
            b: Any = interpret(node.right, sym_tab)
            if node.op == "+":
                return a + b
            elif node.op == "<":
                return a < b
            else:
                raise Exception(f"Unsupported binary operator: {node.op}")

        case ast.Conditional():
            if interpret(node.cond_if):
                return interpret(node.then, sym_tab)
            else:
                return interpret(node.cond_else, sym_tab)
