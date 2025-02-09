from compiler.tokenizer import tokenize
from compiler.parser import parse
from compiler.type_checker import typecheck
from compiler.types import Type, Int
import pytest


def type_check(source_code: str) -> Type:
    return typecheck(parse(tokenize(source_code)))


def test_type_checker_checks_basic_sum() -> None:
    assert type_check("1 + 2") == Int
