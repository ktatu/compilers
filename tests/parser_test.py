from compiler.tokenizer import Token
from compiler.parser import parse
from tests.tokenizer_test import L
import compiler.ast as ast
import pytest


### + - ###
def test_parser_parses_basic_addition() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(ast.Literal(1), "+", ast.Literal(2))


def test_parser_parses_addition_of_multiple_values() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("int_literal", "2", L),
            Token("operator", "+", L),
            Token("int_literal", "1", L),
        ]
    ) == ast.BinaryOp(
        ast.BinaryOp(ast.Literal(1), "+", ast.Literal(2)), "+", ast.Literal(1)
    )


def test_parser_parses_basic_substraction() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "-", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(ast.Literal(1), "-", ast.Literal(2))


### * / ###
def test_parser_parses_basic_multiplication() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "*", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(ast.Literal(1), "*", ast.Literal(2))


def test_parser_parses_basic_division() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "/", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(ast.Literal(1), "/", ast.Literal(2))


def test_parser_parses_parses_multiplication_and_division() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "/", L),
            Token("int_literal", "2", L),
            Token("operator", "*", L),
            Token("int_literal", "3", L),
        ]
    ) == ast.BinaryOp(
        (ast.BinaryOp(ast.Literal(1), "/", ast.Literal(2))), "*", ast.Literal(3)
    )


### PUNCTUATION
def test_parser_parses_parentheses() -> None:
    assert parse(
        [
            Token("punctuation", "(", L),
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("int_literal", "2", L),
            Token("punctuation", ")", L),
        ]
    ) == ast.BinaryOp(ast.Literal(1), "+", ast.Literal(2))


### (1 + 2) * 3 ###
def test_parser_parses_arithmetic_operations_with_parentheses() -> None:
    assert parse(
        [
            Token("punctuation", "(", L),
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("int_literal", "2", L),
            Token("punctuation", ")", L),
            Token("operator", "*", L),
            Token("int_literal", "3", L),
        ]
    ) == ast.BinaryOp(
        ast.BinaryOp(ast.Literal(1), "+", ast.Literal(2)),
        "*",
        ast.Literal(3),
    )


### 3 * (1 + 2) ###
def test_parser_parses_arithmetic_operations_with_parentheses2() -> None:
    assert parse(
        [
            Token("int_literal", "3", L),
            Token("operator", "*", L),
            Token("punctuation", "(", L),
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("int_literal", "2", L),
            Token("punctuation", ")", L),
        ]
    ) == ast.BinaryOp(
        ast.Literal(3), "*", ast.BinaryOp(ast.Literal(1), "+", ast.Literal(2))
    )


### EMPTY TOKEN LIST ###
def test_parser_empty_tokens_list_raises_exception() -> None:
    with pytest.raises(Exception) as exception:
        parse([])

    assert str(exception.value) == "attempting to parse an empty token list"


### UNPARSEABLE ###
def test_parser_fails_to_parse_two_identifiers_next_to_each_other() -> None:
    with pytest.raises(Exception) as exception:
        parse(
            [
                Token("identifier", "a", L),
                Token("operator", "+", L),
                Token("identifier", "b", L),
                Token("identifier", "c", L),
            ]
        )

    assert str(exception.value) == "attempting to parse an empty token list"
