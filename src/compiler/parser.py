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

    # term == identifier or integer literal
    def parse_term() -> ast.Expression:
        # Same structure as in 'parse_expression',
        # but the operators and function calls differ.
        left = parse_factor()

        while peek().text in ["*", "/"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(left, operator, right)

        # anything that should not come right after a term should cause an error
        # tämä on ongelma, koska pitää sallia esim. if a then b else c
        # voidaan tarkastaa onko next_token tunnettujen identifereiden listassa?
        """
        next_token = peek()
        if next_token.type == "identifier":
            raise Exception("two identifiers next to each other in token list")
        """
        return left

    def parse_factor() -> ast.Expression:
        if peek().text == "(":
            return parse_parenthesized()
        elif peek().text == "if":
            return parse_conditional()
        elif peek().type == "int_literal":
            return parse_int_literal()
        elif peek().type == "identifier":
            return parse_identifier()
        else:
            raise Exception(
                f'{peek().location}: expected "(", "if", an integer literal or an identifier'
            )

    def parse_conditional() -> ast.Expression:
        conditional: ast.Conditional = ast.Conditional(
            consume_and_parse("if"), consume_and_parse("then")
        )

        if peek().text == "else":
            consume("else")
            conditional.cond_else = parse_expression()

        return conditional

    def consume_and_parse(keyword_to_consume: str) -> ast.Expression:
        consume(keyword_to_consume)
        return parse_expression()

    def parse_parenthesized() -> ast.Expression:
        consume("(")
        # Recursively call the top level parsing function
        # to parse whatever is inside the parentheses.
        expr = parse_expression()
        consume(")")
        return expr

    parsed_ast = parse_expression()

    # last token always has to be end, otherwise there's tokens that went unhandled
    # this also handles cases like a b + c, not only garbage tokens at the end of list
    last_token = peek()
    if last_token.type != "end":
        raise Exception(
            f"{peek().location}: parsing ended at an unexpected token: {last_token.text}"
        )

    return parsed_ast
