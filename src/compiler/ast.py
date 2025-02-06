from dataclasses import dataclass, field


@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""


@dataclass
class Literal(Expression):
    value: int | bool | None


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
class UnaryOp(Expression):
    op: str
    right: Expression


@dataclass
class Conditional(Expression):
    cond_if: Expression
    then: Expression
    cond_else: Expression | None = None


@dataclass
class Function(Expression):
    # maybe this should just be str?
    name: Identifier
    arguments: list[Expression]


@dataclass
class Block(Expression):
    statements: list[Expression]
    result: Expression | Literal = field(default_factory=lambda: Literal(None))


@dataclass
class VariableDeclaration(Expression):
    name: Identifier
    initialize: Expression
