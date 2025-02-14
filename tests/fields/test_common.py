from lily.fields.common import TextReplacementSetting, apply_text_replacement, apply_text_replacements


class TestApplyTextReplacement:
    def test_plain_text_replacement(self):
        assert apply_text_replacement("Hello world", "world", "there") == "Hello there"
        assert apply_text_replacement("foo bar baz", "bar", "qux") == "foo qux baz"
        assert apply_text_replacement("repeat repeat", "repeat", "once") == "once once"

    def test_no_match_plain_text(self):
        assert apply_text_replacement("Hello world", "mars", "there") == "Hello world"

    def test_regex_replacement(self):
        assert apply_text_replacement("123-456-7890", r"\d{3}-", "XXX-", True) == "XXX-XXX-7890"
        assert apply_text_replacement("abc123xyz", r"\d+", "###", True) == "abc###xyz"
        assert apply_text_replacement("helloHELLOhello", r"hello", "hi", True) == "hiHELLOhi"

    def test_no_match_regex(self):
        assert apply_text_replacement("abcdef", r"\d+", "###", True) == "abcdef"

    def test_empty_strings(self):
        assert apply_text_replacement("", "a", "b") == ""
        # cspell:disable
        # Surprisingly, this is the expected behavior
        assert apply_text_replacement("hello", "", "b") == "bhbeblblbob"
        # Surprisingly, this is the expected behavior
        assert apply_text_replacement("hello", "", "b", True) == "bhbeblblbob"
        # cspell:enable

    def test_regex_capture_groups(self):
        assert (
            apply_text_replacement("My name is John Doe", r"My name is (\w+) (\w+)", r"I am \2, \1", True)
            == "I am Doe, John"
        )
        assert apply_text_replacement("Order ID: 12345", r"Order ID: (\d+)", r"ID: [\1]", True) == "ID: [12345]"


class TestApplyTextReplacements:
    def test_multiple_replacements(self):
        settings = [
            TextReplacementSetting(find="Hello", replace="Hi"),
            TextReplacementSetting(find="world", replace="there"),
        ]
        assert apply_text_replacements("Hello world", settings) == "Hi there"

    def test_regex_replacements(self):
        settings = [
            TextReplacementSetting(find=r"\d+", replace="###", use_regex=True),
            TextReplacementSetting(find=r"abc", replace="xyz", use_regex=True),
        ]
        assert apply_text_replacements("abc123def", settings) == "xyz###def"

    def test_no_settings(self):
        assert apply_text_replacements("No change", None) == "No change"

    def test_empty_settings_list(self):
        assert apply_text_replacements("No change", []) == "No change"

    def test_capture_groups_in_replacements(self):
        settings = [
            TextReplacementSetting(find=r"(\w+) (\w+)", replace=r"\2, \1", use_regex=True),
        ]
        assert apply_text_replacements("John Doe", settings) == "Doe, John"
