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


### * / % ###
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


def test_parser_parses_remainder_operation() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "%", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(ast.Literal(1), "%", ast.Literal(2))


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


### < > <= >= ###
def test_parser_parses_basic_comparison_operations() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "<", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(ast.Identifier("a"), "<", ast.Identifier("b"))

    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "<=", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(ast.Identifier("a"), "<=", ast.Identifier("b"))

    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", ">", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(ast.Identifier("a"), ">", ast.Identifier("b"))

    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", ">=", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(ast.Identifier("a"), ">=", ast.Identifier("b"))


def test_parser_parses_multiple_comparison_operations() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "<", L),
            Token("identifier", "b", L),
            Token("operator", ">", L),
            Token("identifier", "c", L),
        ]
    ) == ast.BinaryOp(
        ast.BinaryOp(ast.Identifier("a"), "<", ast.Identifier("b")),
        ">",
        ast.Identifier("c"),
    )


def test_parser_parses_comparison_operators_with_parentheses() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "<=", L),
            Token("punctuation", "(", L),
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("int_literal", "2", L),
            Token("punctuation", ")", L),
            Token("operator", ">", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(
        ast.BinaryOp(
            ast.Identifier("a"), "<=", ast.BinaryOp(ast.Literal(1), "+", ast.Literal(2))
        ),
        ">",
        ast.Identifier("b"),
    )


### = (assignment) ###
def test_parser_parses_basic_assignment() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "=", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(ast.Identifier("a"), "=", ast.Identifier("b"))


def test_parser_parses_multiple_assignments() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "=", L),
            Token("identifier", "b", L),
            Token("operator", "=", L),
            Token("identifier", "c", L),
        ]
    ) == ast.BinaryOp(
        ast.Identifier("a"),
        "=",
        ast.BinaryOp(ast.Identifier("b"), "=", ast.Identifier("c")),
    )


### != == ###
def test_parser_parses_basic_equality_operation() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "==", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(ast.Identifier("a"), "==", ast.Identifier("b"))


def test_parser_parses_basic_not_equal_operation() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "!=", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(ast.Identifier("a"), "!=", ast.Identifier("b"))


### and ###
def test_parser_parses_basic_and_operation() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "and", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(ast.Identifier("a"), "and", ast.Identifier("b"))


def test_parser_parses_basic_and_operation2() -> None:

    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "and", L),
            Token("identifier", "b", L),
            Token("operator", "+", L),
            Token("identifier", "c", L),
        ]
    ) == ast.BinaryOp(
        ast.Identifier("a"),
        "and",
        ast.BinaryOp(ast.Identifier("b"), "+", ast.Identifier("c")),
    )


## UNARY OPERATIONS ###
def test_parser_parses_unary_not() -> None:
    assert parse(
        [Token("operator", "not", L), Token("identifier", "a", L)]
    ) == ast.UnaryOp("not", ast.Identifier("a"))


def test_parser_parses_unary_minus() -> None:
    assert parse(
        [Token("operator", "-", L), Token("identifier", "a", L)]
    ) == ast.UnaryOp("-", ast.Identifier("a"))


def test_parser_parses_nested_unaries() -> None:
    assert parse(
        [
            Token("operator", "-", L),
            Token("operator", "not", L),
            Token("identifier", "a", L),
        ]
    ) == ast.UnaryOp("-", ast.UnaryOp("not", ast.Identifier("a")))


def test_parser_parses_unary_with_parentheses() -> None:
    assert parse(
        [
            Token("operator", "not", L),
            Token("punctuation", "(", L),
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("int_literal", "2", L),
            Token("punctuation", ")", L),
        ]
    ) == ast.UnaryOp("not", ast.BinaryOp(ast.Literal(1), "+", ast.Literal(2)))


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


### CONDITIONAL ###
def test_parser_parses_basic_conditional() -> None:
    assert parse(
        [
            Token("identifier", "if", L),
            Token("identifier", "a", L),
            Token("identifier", "then", L),
            Token("identifier", "b", L),
            Token("identifier", "else", L),
            Token("identifier", "c", L),
        ]
    ) == ast.Conditional(ast.Identifier("a"), ast.Identifier("b"), ast.Identifier("c"))


def test_parser_parses_conditional_without_else() -> None:
    assert parse(
        [
            Token("identifier", "if", L),
            Token("identifier", "a", L),
            Token("identifier", "then", L),
            Token("identifier", "b", L),
        ]
    ) == ast.Conditional(ast.Identifier("a"), ast.Identifier("b"), None)


def test_parser_parses_conditional_within_expression() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("identifier", "if", L),
            Token("identifier", "a", L),
            Token("identifier", "then", L),
            Token("identifier", "b", L),
            Token("identifier", "else", L),
            Token("identifier", "c", L),
        ]
    ) == ast.BinaryOp(
        ast.Literal(1),
        "+",
        ast.Conditional(ast.Identifier("a"), ast.Identifier("b"), ast.Identifier("c")),
    )


def test_parser_parses_nested_conditionals() -> None:
    assert parse(
        [
            Token("identifier", "if", L),
            Token("identifier", "if", L),
            Token("identifier", "a", L),
            Token("identifier", "then", L),
            Token("identifier", "b", L),
            Token("identifier", "else", L),
            Token("identifier", "c", L),
            Token("identifier", "then", L),
            Token("identifier", "d", L),
            Token("identifier", "else", L),
            Token("identifier", "e", L),
        ]
    )


### FUNCTION ###
def test_parser_parses_function() -> None:
    assert parse(
        [
            Token("identifier", "f", L),
            Token("punctuation", "(", L),
            Token("identifier", "a", L),
            Token("punctuation", ")", L),
        ]
    ) == ast.Function(ast.Identifier("f"), [ast.Identifier("a")])


def test_parser_parses_function_with_multiple_args() -> None:
    assert parse(
        [
            Token("identifier", "f", L),
            Token("punctuation", "(", L),
            Token("identifier", "a", L),
            Token("punctuation", ",", L),
            Token("identifier", "b", L),
            Token("punctuation", ")", L),
        ]
    ) == ast.Function(ast.Identifier("f"), [ast.Identifier("a"), ast.Identifier("b")])


def test_parser_parses_expressions_as_function_args() -> None:
    assert parse(
        [
            Token("identifier", "f", L),
            Token("punctuation", "(", L),
            Token("identifier", "a", L),
            Token("operator", "+", L),
            Token("identifier", "b", L),
            Token("punctuation", ",", L),
            Token("int_literal", "1", L),
            Token("punctuation", ")", L),
        ]
    ) == ast.Function(
        ast.Identifier("f"),
        [ast.BinaryOp(ast.Identifier("a"), "+", ast.Identifier("b")), ast.Literal(1)],
    )


### BLOCK ###
def test_parser_parses_basic_block() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("identifier", "a", L),
            Token("punctuation", ";", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block([ast.Identifier("a")], ast.Literal(None))


def test_parser_parses_block_with_result() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("identifier", "a", L),
            Token("punctuation", ";", L),
            Token("identifier", "b", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block([ast.Identifier("a")], ast.Identifier("b"))


def test_parser_fails_to_parse_block_with_missing_semicolon() -> None:
    with pytest.raises(Exception) as exception:
        parse(
            [
                Token("punctuation", "{", L),
                Token("identifier", "a", L),
                Token("identifier", "b", L),
                Token("punctuation", "}", L),
            ]
        )

    assert str(exception.value) == f'{L}: expected "}}"'


### EMPTY TOKEN LIST ###
def test_parser_empty_tokens_list_raises_exception() -> None:
    with pytest.raises(Exception) as exception:
        parse([])

    assert str(exception.value) == "attempting to parse an empty token list"


### UNPARSEABLE ###
def test_parser_fails_to_parse_two_identifiers_next_to_each_other1() -> None:
    with pytest.raises(Exception) as exception:
        parse(
            [
                Token("identifier", "a", L),
                Token("identifier", "b", L),
                Token("operator", "+", L),
                Token("identifier", "c", L),
            ]
        )

    assert str(exception.value) == f"{L}: parsing ended at an unexpected token: b"


def test_parser_fails_to_parse_two_identifiers_next_to_each_other2() -> None:
    with pytest.raises(Exception) as exception:
        parse(
            [
                Token("identifier", "a", L),
                Token("operator", "+", L),
                Token("identifier", "b", L),
                Token("identifier", "c", L),
            ]
        )

    assert str(exception.value) == f"{L}: parsing ended at an unexpected token: c"


def test_parser_fails_when_left_parenthesis_missing() -> None:
    with pytest.raises(Exception) as exception:
        parse(
            [
                Token("identifier", "a", L),
                Token("operator", "+", L),
                Token("identifier", "b", L),
                Token("punctuation", ")", L),
            ]
        )

    assert str(exception.value) == f"{L}: parsing ended at an unexpected token: )"


def test_parser_fails_when_right_parenthesis_missing() -> None:
    with pytest.raises(Exception) as exception:
        parse(
            [
                Token("punctuation", "(", L),
                Token("identifier", "a", L),
                Token("operator", "+", L),
                Token("identifier", "b", L),
            ]
        )

    assert str(exception.value) == f'{L}: expected ")"'
