from main import Solver


class TestAddToNegative:
    def test_add_letter_to_empty_negative(self):
        solver = Solver("foo\nbar")
        solver.add_to_negative("a")
        assert len(solver.negative_letters) == 1
        assert "a" in solver.negative_letters

    def test_add_letter_that_already_exists(self):
        solver = Solver("foo\nbar")
        solver.add_to_negative("a")
        solver.add_to_negative("a")
        assert len(solver.negative_letters) == 1
        assert "a" in solver.negative_letters

    def test_add_empty_string(self):
        solver = Solver("foo\nbar")
        solver.add_to_negative("")
        assert len(solver.negative_letters) == 0

    def test_add_multiple_letters(self):
        solver = Solver("foo\nbar")
        solver.add_to_negative("abc")
        assert len(solver.negative_letters) == 3
        assert "a" in solver.negative_letters
        assert "c" in solver.negative_letters


class TestFindWords:
    def test_find_words_with_no_pattern_set(self):
        solver = Solver("foo\nbar")
        assert solver.find_words() == ["foo", "bar"]

    def test_find_words_with_all_unknown(self):
        solver = Solver("foo\nbar\nbaz")
        solver.parse_input("? ? ?")
        assert solver.pattern == "..."
        assert solver.find_words() == ["foo", "bar", "baz"]

    def test_find_words_with_one_known(self):
        solver = Solver("foo\nbar\nbaz")
        solver.parse_input("? a ?")
        assert solver.pattern == ".a."
        assert solver.find_words() == ["bar", "baz"]

    def test_find_words_with_one_in_wrong_position(self):
        solver = Solver("foo\nbar\nbaz")
        solver.parse_input("? ? ?a")
        assert solver.pattern == "..[^a]"
        assert solver.find_words() == ["bar", "baz"]


class TestParseInput:
    def test_input_with_completely_unknown(self):
        solver = Solver("foo\nbar")
        solver.parse_input("? ? ?")
        assert solver.pattern == "..."

    def test_input_with_letter_in_wrong_position(self):
        solver = Solver("foo\nbar")
        solver.parse_input("?a ? ?")
        assert solver.pattern == "[^a].."
        assert solver.required_letters == {"a"}
        assert solver.not_at_position == ["a", "", "", "", ""]

    def test_input_with_all_known(self):
        solver = Solver("foo\nbar")
        solver.parse_input("f o o")
        assert solver.pattern == "foo"

    def test_required_and_nap_is_retained(self):
        solver = Solver("foo\nbar\nbaz")
        solver.parse_input("?a ? ?")
        assert solver.required_letters == {"a"}
        solver.parse_input("? ?z ?")
        assert solver.required_letters == {"a", "z"}
        assert solver.not_at_position == ["a", "z", "", "", ""]
