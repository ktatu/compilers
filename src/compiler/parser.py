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

    def parse_identifier() -> ast.Identifier | ast.Function:
        if peek().type != "identifier":
            raise Exception(f"{peek().location}: expected an identifier")
        token = consume()

        if peek().text == "(":
            return parse_function(token.text)

        return ast.Identifier(str(token.text))

    def parse_expression() -> ast.Expression:
        return parse_assignment()

    def parse_assignment() -> ast.Expression:
        left = parse_or()

        if peek().text == "=":
            operator_token = consume()
            operator = operator_token.text

            right = parse_assignment()
            left = ast.BinaryOp(left, operator, right)

        return left

    def parse_or() -> ast.Expression:
        left = parse_and()

        while peek().text == "and":
            operator_token = consume()
            operator = operator_token.text
            right = parse_and()
            left = ast.BinaryOp(left, operator, right)

        return left

    def parse_and() -> ast.Expression:
        left = parse_equality()

        while peek().text == "and":
            operator_token = consume()
            operator = operator_token.text
            right = parse_equality()
            left = ast.BinaryOp(left, operator, right)

        return left

    def parse_equality() -> ast.Expression:
        left = parse_comparison()

        while peek().text in ["!=", "=="]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_comparison()
            left = ast.BinaryOp(left, operator, right)

        return left

    def parse_comparison() -> ast.Expression:
        left = parse_arithmetic()

        while peek().text in ["<", "<=", ">", ">="]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_arithmetic()
            left = ast.BinaryOp(left, operator, right)

        return left

    def parse_arithmetic() -> ast.Expression:
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

        while peek().text in ["*", "/", "%"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(left, operator, right)

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
        # should be above parse_factor in precedence, but does having it here cause anything?
        # other option: parse_term calls parse_operation that calls parse_factor
        elif peek().text in ["not", "-"]:
            return parse_unary_operation()
        else:
            raise Exception(
                f'{peek().location}: expected "(", "if", an integer literal or an identifier'
            )

    def parse_unary_operation() -> ast.UnaryOp:
        unary_operator = consume().text
        expr = parse_expression()

        return ast.UnaryOp(unary_operator, expr)

    def parse_conditional() -> ast.Conditional:
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

    def parse_function(function_name: str) -> ast.Function:
        args: list[ast.Expression] = []

        consume("(")

        first_arg = parse_expression()
        args.append(first_arg)

        while peek().text == ",":
            consume(",")

            arg = parse_expression()
            args.append(arg)

        consume(")")

        return ast.Function(ast.Identifier(function_name), args)

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
