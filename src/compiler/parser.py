from compiler.tokenizer import Token
import compiler.ast as ast


def parse(tokens: list[Token]) -> ast.Expression:
    pos = 0

    def peek() -> Token:
        if pos < len(tokens):
            return tokens[pos]
        elif len(tokens) == 0:
            raise Exception("attempting to parse an empty token list")
        else:
            return Token(
                location=tokens[-1].location,
                type="end",
                text="",
            )

    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos

        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise Exception(f'{token.location}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise Exception(f"{token.location}: expected one of: {comma_separated}")
        pos += 1

        return token

    def parse_int_literal() -> ast.Literal:
        if peek().type != "int_literal":
            raise Exception(f"{peek().location}: expected an integer literal")
        token = consume()

        return ast.Literal(int(token.text))

    def parse_identifier() -> ast.Identifier:
        if peek().type != "identifier":
            raise Exception(f"{peek().location}: expected an identifier")
        token = consume()

        return ast.Identifier(str(token.text))

    def parse_expression() -> ast.Expression:
        # Same as before
        left = parse_term()
        while peek().text in ["+", "-"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_term()
            left = ast.BinaryOp(left, operator, right)
        return left

    def parse_term() -> ast.Expression:
        # Same structure as in 'parse_expression',
        # but the operators and function calls differ.
        left = parse_factor()
        while peek().text in ["*", "/"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(left, operator, right)
        return left

    def parse_factor() -> ast.Expression:
        if peek().text == "(":
            return parse_parenthesized()
        elif peek().type == "int_literal":
            return parse_int_literal()
        elif peek().type == "identifier":
            return parse_identifier()
        else:
            raise Exception(
                f'{peek().location}: expected "(", an integer literal or an identifier'
            )

    def parse_parenthesized() -> ast.Expression:
        consume("(")
        # Recursively call the top level parsing function
        # to parse whatever is inside the parentheses.
        expr = parse_expression()
        consume(")")
        return expr

    return_val = parse_expression()
    print(return_val)
    return return_val
