from dataclasses import dataclass
import re
from typing import Literal


@dataclass(frozen=True)
class Location:
    column: int
    line: int


TokenType = Literal["int_literal", "identifier", "operator", "punctuation", "end"]


@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str
    location: Location


# Operators: +, -, *, /, =, ==, !=, <, <=, >, >=
# this still allows things like test- to pass as identifiers, which should be two tokens: test and -
def tokenize(source_code: str) -> list[Token]:
    newline_re = re.compile(r"\n")
    whitespace_re = re.compile(r"\s")
    comment_re = re.compile(r"(//|#).*\n")
    # maybe \b shouldnt be at the start? might break something later
    identifier_re = re.compile(r"\b[A-Za-z_][A-Za-z_0-9]*")
    integer_literal_re = re.compile(r"[0-9]+")
    operator_re = re.compile(r"(==|<=|>=|!=|\+|-|\*|/|=|>|<|%|not|and|or)")
    punctuation_re = re.compile(r"[(){},;:]")

    position = 0
    # the current column is position - column_start_pos
    # column_start_pos == where column 0 is on the current line, as a position value
    column_start_pos = 0
    line = 0

    tokens: list[Token] = []

    def regexMatch(pattern: re.Pattern[str], type: TokenType) -> bool:
        nonlocal position

        match = pattern.match(source_code, position)
        if match is not None:
            tokens.append(
                Token(
                    type=type,
                    text=source_code[position : match.end()],
                    location=Location(column=position - column_start_pos, line=line),
                )
            )
            position = match.end()
            return True
        return False

    while position < len(source_code):

        match = comment_re.match(source_code, position)
        if match is not None:
            position = match.end()
            column_start_pos = match.end()
            line += 1
            continue

        match = newline_re.match(source_code, position)
        if match is not None:
            position = match.end()
            column_start_pos = match.end()
            line += 1
            continue

        match = whitespace_re.match(source_code, position)
        if match is not None:
            position = match.end()
            continue

        if regexMatch(operator_re, "operator"):
            continue

        if regexMatch(identifier_re, "identifier"):
            continue

        if regexMatch(integer_literal_re, "int_literal"):
            continue

        if regexMatch(punctuation_re, "punctuation"):
            continue

        raise Exception(
            "No match found, position: ",
            position,
            ", source code at position: ",
            source_code[position],
        )

    return tokens
