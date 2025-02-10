from compiler.tokenizer import tokenize
from compiler.parser import parse
from compiler.type_checker import typecheck
from compiler.types import *
import pytest


def type_check(source_code: str) -> Type:
    return typecheck(parse(tokenize(source_code)))


### BINARY OPERATION ###
def test_type_basic_arithmetic() -> None:
    assert type_check("1 + 2") == Int
    assert type_check("1 - 2") == Int
    assert type_check("1 * 2") == Int
    assert type_check("1 / 2") == Int


def test_type_basic_comparisons() -> None:
    assert type_check("1 < 2") == Bool
    assert type_check("1 <= 2") == Bool
    assert type_check("1 > 2") == Bool
    assert type_check("1 >= 2") == Bool


def test_type_or() -> None:
    assert type_check("true or false") == Bool


def test_type_assignment() -> None:
    assert type_check("var x = 5; x = 10") == Unit


def test_type_equality() -> None:
    assert type_check("var x = 5; var y = 10; x == y") == Bool
    assert type_check("var x = 5; var y = 10; x != y") == Bool


### UNARY OPERATION ###
def test_type_unary_operation() -> None:
    assert type_check("not true") == Bool
    assert type_check("var x = true; not x") == Bool
    assert type_check("- 5") == Int
    assert type_check("var x = 5; - x") == Int


### CONDITIONAL ###
def test_type_conditionals() -> None:
    assert type_check("if true then 1 else 2") == Int
    assert type_check("if true then true else false") == Bool


### VARIABLE DECLARATION ###
def test_type_for_variable_declaration_is_unit() -> None:
    assert type_check("var x = 5") == Unit


### IDENTIFIER ###
def test_type_declared_identifier() -> None:
    assert type_check("var x = 5; x") == Int


### BLOCK ###
def test_type_for_block_with_no_result_is_unit() -> None:
    assert type_check(f"{{ 1; 2; 3; }}") == Unit
    assert type_check("1; 2; 3;") == Unit


def test_type_for_block_with_result() -> None:
    assert type_check(f"{{ 1; 2; 3 }}") == Int
    assert type_check("1; 2; 3") == Int


def test_type_for_empty_block_is_unit() -> None:
    assert type_check(f"{{}}") == Unit


def test_type_empty_block_and_result() -> None:
    assert type_check(f"{{}}; 5") == Int
