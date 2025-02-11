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


### TYPED VARIABLE DECLARATION ###
def test_type_for_typed_var_declaration_is_unit() -> None:
    assert type_check("var x: Int = 5") == Unit
    assert type_check("var x: Int = 1 + 1") == Unit
    assert type_check("var x: Bool = false") == Unit
    assert type_check("var x: Bool = true") == Unit


def test_type_check_fails_when_declared_type_does_not_match_initializer() -> None:
    with pytest.raises(Exception) as e1:
        type_check("var x: Int = true")

    assert "declared type of a variable does not match type checked type" in str(
        e1.value
    )

    with pytest.raises(Exception) as e2:
        type_check("var x: Bool = 5")

    assert "declared type of a variable does not match type checked type" in str(
        e2.value
    )


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


### WHILE ###
def test_type_while_loop() -> None:
    assert type_check("while true do 5") == Unit


def test_type_while_loop_fails_when_body_typecheck_fails() -> None:
    with pytest.raises(Exception) as e:
        type_check("while true do x")

    assert "Type check error: could not find type for symbol" in str(e.value)


### FUNCTION CALL ###
def test_type_of_built_in_functions() -> None:
    assert type_check("print_int(5)") == Unit
    assert type_check("print_bool(false)") == Unit
    assert type_check("read_int(5)") == Unit

    with pytest.raises(Exception) as e1:
        type_check("print_int(true)")

    assert "types of function arguments do not match expected types" in str(e1.value)
