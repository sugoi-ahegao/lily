import unidecode


def to_ascii(text: str) -> str:
    return unidecode.unidecode(text, errors="preserve")


def test_unidecode() -> None:
    assert to_ascii("é") == "e"
    assert to_ascii("e") == "e"
