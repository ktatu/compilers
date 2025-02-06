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

        return ast.Literal(token.location, int(token.text))

    def parse_identifier() -> ast.Identifier | ast.Function:
        if peek().type != "identifier":
            raise Exception(f"{peek().location}: expected an identifier")
        if peek().text == "var":
            raise Exception(
                f"{peek().location}: attempting to declare a variable outside top-level scope"
            )

        token = consume()

        if peek().text == "(":
            return parse_function(token)

        return ast.Identifier(token.location, str(token.text))

    def parse_expression(allow_var_parsing=False) -> ast.Expression:
        if allow_var_parsing and peek().text == "var":
            return parse_variable_declaration()

        return parse_assignment()

    def parse_assignment() -> ast.Expression:
        left = parse_or()

        if peek().text == "=":
            operator_token = consume()
            operator = operator_token.text

            right = parse_assignment()
            left = ast.BinaryOp(operator_token.location, left, operator, right)

        return left

    def parse_or() -> ast.Expression:
        left = parse_and()

        while peek().text == "and":
            operator_token = consume()
            operator = operator_token.text
            right = parse_and()
            left = ast.BinaryOp(operator_token.location, left, operator, right)

        return left

    def parse_and() -> ast.Expression:
        left = parse_equality()

        while peek().text == "and":
            operator_token = consume()
            operator = operator_token.text
            right = parse_equality()
            left = ast.BinaryOp(operator_token.location, left, operator, right)

        return left

    def parse_equality() -> ast.Expression:
        left = parse_comparison()

        while peek().text in ["!=", "=="]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_comparison()
            left = ast.BinaryOp(operator_token.location, left, operator, right)

        return left

    def parse_comparison() -> ast.Expression:
        left = parse_arithmetic()

        while peek().text in ["<", "<=", ">", ">="]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_arithmetic()
            left = ast.BinaryOp(operator_token.location, left, operator, right)

        return left

    def parse_arithmetic() -> ast.Expression:
        left = parse_term()

        while peek().text in ["+", "-"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_term()
            left = ast.BinaryOp(operator_token.location, left, operator, right)

        return left

    def parse_term() -> ast.Expression:
        left = parse_factor()

        while peek().text in ["*", "/", "%"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(operator_token.location, left, operator, right)

        return left

    """
    def parse_unary() -> ast.Expression:
        left = parse_factor()

        while peek().text in ["not", "-"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(left, operator, right)

        return left
    """

    def parse_factor() -> ast.Expression:
        if peek().text == "(":
            return parse_parenthesized()
        elif peek().text == "if":
            return parse_conditional()
        elif peek().type == "int_literal":
            return parse_int_literal()
        # all identifiers are treated the same in the tokenizer
        # therefore known identifiers (while, var, ...) need to be handled before this
        elif peek().type == "identifier":
            return parse_identifier()
        # should be above parse_factor in precedence, but does having it here cause anything?
        # other option: parse_term calls parse_operation that calls parse_factor
        elif peek().text in ["not", "-"]:
            return parse_unary_operation()
        elif peek().text == "{":
            return parse_block()
        else:
            raise Exception(
                f'{peek().location}: expected "(", "if", an integer literal or an identifier'
            )

    def parse_unary_operation() -> ast.UnaryOp:
        operator_token = consume()
        expr = parse_expression()

        return ast.UnaryOp(operator_token.location, operator_token.text, expr)

    def parse_conditional() -> ast.Conditional:
        if_token = consume("if")
        if_expr = parse_expression()

        consume("then")
        then_expr = parse_expression()

        if peek().text == "else":
            consume("else")
            else_expr = parse_expression()
            return ast.Conditional(if_token.location, if_expr, then_expr, else_expr)

        return ast.Conditional(if_token.location, if_expr, then_expr)

    def parse_function(function_token: Token) -> ast.Function:
        args: list[ast.Expression] = []
        consume("(")

        first_arg = parse_expression()
        args.append(first_arg)

        while peek().text == ",":
            consume(",")

            arg = parse_expression()
            args.append(arg)

        consume(")")

        return ast.Function(function_token.location, function_token.text, args)

    def parse_parenthesized() -> ast.Expression:
        consume("(")
        expr = parse_expression()
        consume(")")
        return expr

    # in inner blocks, missing ; after } is allowed
    def parse_block() -> ast.Block:
        expressions: list[ast.Expression] = []
        block_token = consume("{")

        no_result_expr = False
        while peek().text != "}":
            expr = parse_expression(True)
            expressions.append(expr)

            try:
                consume(";")
                no_result_expr = True
            except Exception as e:
                if isinstance(expr, ast.Block) or peek().text == "}":
                    no_result_expr = False
                    continue
                raise

        consume("}")

        if no_result_expr:
            return ast.Block(block_token.location, expressions)

        result = expressions.pop()
        return ast.Block(block_token.location, expressions, result)

    def parse_variable_declaration() -> ast.Expression:
        var_token = consume("var")
        identifier: ast.Identifier = parse_identifier()
        consume("=")
        expr = parse_expression()

        return ast.VariableDeclaration(var_token.location, identifier.name, expr)

    parsed_ast = parse_expression(True)
    # print("--------")
    # print(parsed_ast)
    # print("--------")

    # last token always has to be end, otherwise there's tokens that went unhandled
    # this also handles cases like a b + c, not only garbage tokens at the end of list
    last_token = peek()
    if last_token.type != "end":
        raise Exception(
            f"{peek().location}: parsing ended at an unexpected token: {last_token.text}"
        )

    return parsed_ast
