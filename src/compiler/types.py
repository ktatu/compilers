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


Arithmetic = FunType((Int, Int), Int)
Comparison = FunType((Int, Int), Bool)
AndOr = FunType((Bool, Bool), Bool)

PrintBool = FunType((Bool), Unit)
PrintInt = FunType((Int), Unit)
# not sure about this one
ReadInt = FunType((Int), Unit)
