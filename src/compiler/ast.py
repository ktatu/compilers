from dataclasses import dataclass, field
from compiler.tokenizer import Location
from compiler.types import Type


@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""

    location: Location


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
class UnaryOp(Expression):
    op: str
    right: Expression


@dataclass
class Conditional(Expression):
    cond_if: Expression
    then: Expression
    cond_else: Expression | None = None


@dataclass
class FunctionCall(Expression):
    name: str
    arguments: list[Expression]


@dataclass
class Block(Expression):
    statements: list[Expression]
    result: Expression | Literal = field(
        default_factory=lambda: Literal(location=None, value=None)
    )


@dataclass
class VariableDeclaration(Expression):
    name: str
    initializer: Expression
    declared_type: Type = None


@dataclass
class While(Expression):
    cond: Expression
    body: Expression
