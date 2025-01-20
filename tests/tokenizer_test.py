from dataclasses import dataclass
from compiler.tokenizer import Location, Token, tokenize


@dataclass(frozen=True)
class LocationTest(Location):
    def __eq__(self, other: object) -> bool:
        return True


L = LocationTest(column=0, line=0)


### WHITESPACE ###
def test_tokenizer_skips_whitespace() -> None:
    assert tokenize("   \n  \n ") == []


### IDENTIFIERS ###
def test_tokenizer_recognizes_an_identifier() -> None:
    assert tokenize(" test ") == [Token(type="identifier", text="test", location=L)]


def test_tokenizer_recognizes_multiple_identifiers() -> None:
    assert tokenize("if var_name \n while") == [
        Token(type="identifier", text="if", location=L),
        Token(type="identifier", text="var_name", location=L),
        Token(type="identifier", text="while", location=L),
    ]


### INTEGER_LITERALS ###
def test_tokenizer_recognizes_integer_literal() -> None:
    assert tokenize("123") == [Token(type="int_literal", text="123", location=L)]


def test_tokenizer_recognizes_multiple_integer_literals() -> None:
    assert tokenize(" 123 555") == [
        Token(type="int_literal", text="123", location=L),
        Token(type="int_literal", text="555", location=L),
    ]
