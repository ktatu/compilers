from dataclasses import dataclass


@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""


@dataclass
class Literal(Expression):
    value: int | bool


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class BinaryOp(Expression):
    """AST node for a binary operation like `A + B`"""

    left: Expression
    op: str
    right: Expression


@dataclass
class Conditional(Expression):
    cond_if: Expression
    then: Expression
    cond_else: Expression | None = None


@dataclass
class Function(Expression):
    name: Identifier
    arguments: list[Expression]
