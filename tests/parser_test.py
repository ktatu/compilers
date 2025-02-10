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
    ) == ast.BinaryOp(L, ast.Literal(L, 1), "+", ast.Literal(L, 2))


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
        L,
        ast.BinaryOp(L, ast.Literal(L, 1), "+", ast.Literal(L, 2)),
        "+",
        ast.Literal(L, 1),
    )


def test_parser_parses_basic_substraction() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "-", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(L, ast.Literal(L, 1), "-", ast.Literal(L, 2))


### * / % ###
def test_parser_parses_basic_multiplication() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "*", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(L, ast.Literal(L, 1), "*", ast.Literal(L, 2))


def test_parser_parses_basic_division() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "/", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(L, ast.Literal(L, 1), "/", ast.Literal(L, 2))


def test_parser_parses_remainder_operation() -> None:
    assert parse(
        [
            Token("int_literal", "1", L),
            Token("operator", "%", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.BinaryOp(L, ast.Literal(L, 1), "%", ast.Literal(L, 2))


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
        L,
        (ast.BinaryOp(L, ast.Literal(L, 1), "/", ast.Literal(L, 2))),
        "*",
        ast.Literal(L, 3),
    )


### < > <= >= ###
def test_parser_parses_basic_comparison_operations() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "<", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(L, ast.Identifier(L, "a"), "<", ast.Identifier(L, "b"))

    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "<=", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(L, ast.Identifier(L, "a"), "<=", ast.Identifier(L, "b"))

    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", ">", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(L, ast.Identifier(L, "a"), ">", ast.Identifier(L, "b"))

    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", ">=", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(L, ast.Identifier(L, "a"), ">=", ast.Identifier(L, "b"))


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
        L,
        ast.BinaryOp(L, ast.Identifier(L, "a"), "<", ast.Identifier(L, "b")),
        ">",
        ast.Identifier(L, "c"),
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
        L,
        ast.BinaryOp(
            L,
            ast.Identifier(L, "a"),
            "<=",
            ast.BinaryOp(L, ast.Literal(L, 1), "+", ast.Literal(L, 2)),
        ),
        ">",
        ast.Identifier(L, "b"),
    )


### = (assignment) ###
def test_parser_parses_basic_assignment() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "=", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(L, ast.Identifier(L, "a"), "=", ast.Identifier(L, "b"))


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
        L,
        ast.Identifier(L, "a"),
        "=",
        ast.BinaryOp(
            L,
            ast.Identifier(L, "b"),
            "=",
            ast.Identifier(L, "c"),
        ),
    )


def test_parser_parses_variable_reassignment() -> None:
    assert parse(
        [
            Token("identifier", "var", L),
            Token("identifier", "x", L),
            Token("operator", "=", L),
            Token("int_literal", "5", L),
            Token("punctuation", ";", L),
            Token("identifier", "x", L),
            Token("operator", "=", L),
            Token("int_literal", "10", L),
        ]
    ) == ast.Block(
        L,
        [ast.VariableDeclaration(L, "x", ast.Literal(L, 5))],
        ast.BinaryOp(L, ast.Identifier(L, "x"), "=", ast.Literal(L, 10)),
    )


### != == ###
def test_parser_parses_basic_equality_operation() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "==", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(L, ast.Identifier(L, "a"), "==", ast.Identifier(L, "b"))


def test_parser_parses_basic_not_equal_operation() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "!=", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(L, ast.Identifier(L, "a"), "!=", ast.Identifier(L, "b"))


### and ###
def test_parser_parses_basic_and_operation() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("operator", "and", L),
            Token("identifier", "b", L),
        ]
    ) == ast.BinaryOp(L, ast.Identifier(L, "a"), "and", ast.Identifier(L, "b"))


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
        L,
        ast.Identifier(L, "a"),
        "and",
        ast.BinaryOp(
            L,
            ast.Identifier(L, "b"),
            "+",
            ast.Identifier(L, "c"),
        ),
    )


## UNARY OPERATIONS ###
def test_parser_parses_unary_not() -> None:
    assert parse(
        [Token("operator", "not", L), Token("identifier", "a", L)]
    ) == ast.UnaryOp(L, "not", ast.Identifier(L, "a"))


def test_parser_parses_unary_minus() -> None:
    assert parse(
        [Token("operator", "-", L), Token("identifier", "a", L)]
    ) == ast.UnaryOp(L, "-", ast.Identifier(L, "a"))


def test_parser_parses_nested_unaries() -> None:
    assert parse(
        [
            Token("operator", "-", L),
            Token("operator", "not", L),
            Token("identifier", "a", L),
        ]
    ) == ast.UnaryOp(L, "-", ast.UnaryOp(L, "not", ast.Identifier(L, "a")))

    assert parse(
        [
            Token("operator", "not", L),
            Token("operator", "not", L),
            Token("identifier", "a", L),
        ]
    ) == ast.UnaryOp(L, "not", ast.UnaryOp(L, "not", ast.Identifier(L, "a")))


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
    ) == ast.UnaryOp(
        L,
        "not",
        ast.BinaryOp(L, ast.Literal(L, 1), "+", ast.Literal(L, 2)),
    )


def test_parser_parses_unary_of_declared_variable() -> None:
    assert parse(
        [
            Token("identifier", "var", L),
            Token("identifier", "x", L),
            Token("operator", "=", L),
            Token("identifier", "true", L),
            Token("punctuation", ";", L),
            Token("operator", "-", L),
            Token("identifier", "x", L),
        ],
    ) == ast.Block(
        L,
        [ast.VariableDeclaration(L, "x", ast.Literal(L, True))],
        ast.UnaryOp(L, "-", ast.Identifier(L, "x")),
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
    ) == ast.BinaryOp(L, ast.Literal(L, 1), "+", ast.Literal(L, 2))


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
        L,
        ast.BinaryOp(L, ast.Literal(L, 1), "+", ast.Literal(L, 2)),
        "*",
        ast.Literal(L, 3),
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
        L,
        ast.Literal(L, 3),
        "*",
        ast.BinaryOp(L, ast.Literal(L, 1), "+", ast.Literal(L, 2)),
    )


### BOOLEAN ###
def test_parser_parses_basic_boolean() -> None:
    assert parse([Token("identifier", "true", L)]) == ast.Literal(L, True)
    assert parse([Token("identifier", "false", L)]) == ast.Literal(L, False)


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
    ) == ast.Conditional(
        L,
        ast.Identifier(L, "a"),
        ast.Identifier(L, "b"),
        ast.Identifier(L, "c"),
    )


def test_parser_parses_conditional_without_else() -> None:
    assert parse(
        [
            Token("identifier", "if", L),
            Token("identifier", "a", L),
            Token("identifier", "then", L),
            Token("identifier", "b", L),
        ]
    ) == ast.Conditional(L, ast.Identifier(L, "a"), ast.Identifier(L, "b"), None)


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
        L,
        ast.Literal(L, 1),
        "+",
        ast.Conditional(
            L,
            ast.Identifier(L, "a"),
            ast.Identifier(L, "b"),
            ast.Identifier(L, "c"),
        ),
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
    ) == ast.Conditional(
        L,
        ast.Conditional(
            L,
            ast.Identifier(L, "a"),
            ast.Identifier(L, "b"),
            ast.Identifier(L, "c"),
        ),
        ast.Identifier(L, "d"),
        ast.Identifier(L, "e"),
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
    ) == ast.FunctionCall(L, "f", [ast.Identifier(L, "a")])


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
    ) == ast.FunctionCall(L, "f", [ast.Identifier(L, "a"), ast.Identifier(L, "b")])


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
    ) == ast.FunctionCall(
        L,
        "f",
        [
            ast.BinaryOp(
                L,
                ast.Identifier(L, "a"),
                "+",
                ast.Identifier(L, "b"),
            ),
            ast.Literal(L, 1),
        ],
    )


### BLOCK ###
def test_parser_parses_empty_block() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block(L, [], None)


def test_parser_parses_basic_block_with_no_result() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("identifier", "a", L),
            Token("punctuation", ";", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block(L, [ast.Identifier(L, "a")], ast.Literal(None, None))


def test_parser_parses_block_with_result() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("identifier", "a", L),
            Token("punctuation", ";", L),
            Token("identifier", "b", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block(L, [ast.Identifier(L, "a")], ast.Identifier(L, "b"))


def test_parser_parses_basic_block_with_only_result() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("identifier", "a", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block(L, [], ast.Identifier(L, "a"))


def test_parser_parses_block_within_block() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("punctuation", "{", L),
            Token("identifier", "a", L),
            Token("punctuation", "}", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block(L, [], ast.Block(L, [], ast.Identifier(L, "a")))


def test_parser_parses_inner_blocks_with_no_semicolons() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("punctuation", "{", L),
            Token("identifier", "a", L),
            Token("punctuation", "}", L),
            Token("punctuation", "{", L),
            Token("identifier", "b", L),
            Token("punctuation", "}", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block(
        L,
        [ast.Block(L, [], ast.Identifier(L, "a"))],
        ast.Block(L, [], ast.Identifier(L, "b")),
    )


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

    assert str(exception.value) == f'{L}: expected ";"'


### WHILE ###
def test_parser_parses_basic_while_loop() -> None:
    assert parse(
        [
            Token("identifier", "while", L),
            Token("identifier", "x", L),
            Token("identifier", "do", L),
            Token("identifier", "y", L),
        ]
    ) == ast.While(L, ast.Identifier(L, "x"), ast.Identifier(L, "y"))


### VARIABLE DECLARATION ###
def test_parser_parses_basic_variable_declaration() -> None:
    assert parse(
        [
            Token("identifier", "var", L),
            Token("identifier", "x", L),
            Token("operator", "=", L),
            Token("int_literal", "1", L),
        ]
    ) == ast.VariableDeclaration(L, "x", ast.Literal(L, 1))

    assert parse(
        [
            Token("identifier", "var", L),
            Token("identifier", "x", L),
            Token("operator", "=", L),
            Token("int_literal", "1", L),
            Token("operator", "+", L),
            Token("int_literal", "2", L),
        ]
    ) == ast.VariableDeclaration(
        L,
        "x",
        ast.BinaryOp(L, ast.Literal(L, 1), "+", ast.Literal(L, 2)),
    )


def test_parser_parses_var_declaration_inside_block_top_level() -> None:
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("identifier", "var", L),
            Token("identifier", "x", L),
            Token("operator", "=", L),
            Token("int_literal", "1", L),
            Token("punctuation", ";", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block(
        L,
        [ast.VariableDeclaration(L, "x", ast.Literal(L, 1))],
        ast.Literal(L, None),
    )


def test_parser_parses_multiple_var_declarations_in_different_block_top_levels() -> (
    None
):
    assert parse(
        [
            Token("punctuation", "{", L),
            Token("identifier", "var", L),
            Token("identifier", "x", L),
            Token("operator", "=", L),
            Token("int_literal", "1", L),
            Token("punctuation", ";", L),
            Token("identifier", "var", L),
            Token("identifier", "y", L),
            Token("operator", "=", L),
            Token("identifier", "a", L),
            Token("punctuation", ";", L),
            Token("punctuation", "}", L),
        ]
    ) == ast.Block(
        L,
        [
            ast.VariableDeclaration(L, "x", ast.Literal(L, 1)),
            ast.VariableDeclaration(L, "y", ast.Identifier(L, "a")),
        ],
        ast.Literal(L, None),
    )


def test_parser_fails_when_var_declaration_not_in_top_level() -> None:
    with pytest.raises(Exception) as exception:
        parse(
            [
                Token("int_literal", "1", L),
                Token("operator", "+", L),
                Token("identifier", "var", L),
                Token("identifier", "x", L),
                Token("operator", "=", L),
                Token("int_literal", "1", L),
            ]
        )

    assert (
        str(exception.value)
        == f"{L}: attempting to declare a variable outside top-level scope"
    )


### MULTIPLE TOP LEVEL EXPRESSIONS ###
def test_parser_parses_multiple_top_level_expressions_with_no_result() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("punctuation", ";", L),
            Token("identifier", "b", L),
            Token("punctuation", ";", L),
        ]
    ) == ast.Block(
        L, [ast.Identifier(L, "a"), ast.Identifier(L, "b")], ast.Literal(None, None)
    )


def test_parser_parses_multiple_top_level_expressions_with_result() -> None:
    assert parse(
        [
            Token("identifier", "a", L),
            Token("punctuation", ";", L),
            Token("identifier", "b", L),
            Token("punctuation", ";", L),
            Token("identifier", "var", L),
            Token("identifier", "x", L),
            Token("operator", "=", L),
            Token("int_literal", "5", L),
        ]
    ) == ast.Block(
        L,
        [ast.Identifier(L, "a"), ast.Identifier(L, "b")],
        ast.VariableDeclaration(L, "x", ast.Literal(L, 5)),
    )


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
