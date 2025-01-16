from compiler.tokenizer import tokenize

def test_tokenizer_skips_whitespace() -> None:
    assert tokenize("test") == ["test"]