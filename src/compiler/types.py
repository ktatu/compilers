from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Type:
    "Base class"


@dataclass(frozen=True)
class BasicType(Type):
    name: str


Int = BasicType("Int")
Bool = BasicType("Bool")
Unit = BasicType("Unit")


@dataclass(frozen=True)
class FunType(Type):
    argument_types: Tuple[Type, ...]
    return_type: Type
