import re

# this still allows things like test- to pass as identifiers
def tokenize(source_code: str) -> list[str]:
    whitespace_re = re.compile(r"\s+")
    # maybe \b shouldnt be at the start? might break something later
    identifier_re = re.compile(r"\b[A-Za-z_][A-Za-z_0-9]*")
    integer_literal_re = re.compile(r"[0-9]+")

    tokens: list[str] = []
    position = 0

    while position < len(source_code):
        whitespace_match = whitespace_re.match(source_code, position)
        identifier_match = identifier_re.match(source_code, position)
        integer_literal_match = integer_literal_re.match(source_code, position)


        if whitespace_match is not None:
            position = whitespace_match.end()
            continue

        if identifier_match is not None:
            tokens.append(source_code[position:identifier_match.end()])
            position = identifier_match.end()
            continue

        if integer_literal_match is not None:
            tokens.append(source_code[position:integer_literal_match.end()])
            position = integer_literal_match.end()
            continue

        raise Exception("No match found, position: ", position, ", source code at position: ", source_code[position])

    return tokens