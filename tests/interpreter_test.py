from tests.tokenizer_test import L
from compiler.tokenizer import tokenize
from compiler.parser import parse
from compiler.interpreter import Value, interpret


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
