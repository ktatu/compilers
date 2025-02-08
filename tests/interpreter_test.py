from tests.tokenizer_test import L
from compiler.tokenizer import tokenize
from compiler.parser import parse
from compiler.interpreter import Value, interpret
import pytest


def test_interpret(source_code: str) -> Value:
    return interpret(parse(tokenize(source_code)))


### BINARY OPERATIONS ###
def test_interpreter_handles_addition() -> None:
    assert test_interpret("1 + 2") == 3


### CONDITIONAL ###
def test_interpreter_handles_basic_conditionals_with_literals() -> None:
    assert test_interpret("if true then 1 else 2") == 1


### BLOCK ###
def test_interpreter_handles_block_with_no_result() -> None:
    assert test_interpret(f"{{ a; }}") == None


def test_interpreter_handles_block_with_result() -> None:
    assert test_interpret(f"{{ 1 }}") == 1


### BLOCK + IDENTIFIER ###
def test_interpreter_handles_identifier_declared_on_same_level() -> None:
    assert test_interpret("var x = 5; x") == 5


def test_interpreter_throws_exception_when_it_cannot_find_identifier() -> None:
    with pytest.raises(Exception) as e:
        test_interpret("var x = 5; y")

    assert str(e.value) == f"{L}: could not find value for identifier y"
