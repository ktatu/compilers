from compiler.tokenizer import tokenize

### WHITESPACE ###
def test_tokenizer_skips_whitespace() -> None:
    assert tokenize("   \n  \n ") == []
### ###

### IDENTIFIERS ###
def test_tokenizer_recognizes_an_identifier() -> None:
    assert tokenize(" test ") == ["test"]

def test_tokenizer_recognizes_multiple_identifiers() -> None:
    assert tokenize("if var_name \n while") == ["if", "var_name", "while"]
### ###

### INTEGER_LITERALS ###
def test_tokenizer_recognizes_integer_literal() -> None:
    assert tokenize("123") == ["123"]

def test_tokenizer_recognizes_multiple_integer_literals() -> None:
    assert tokenize(" 123 555") == ["123", "555"]
### ###