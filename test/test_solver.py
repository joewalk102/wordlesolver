from main import Solver


class TestReconcileNegatives:
    def test_required_letter_in_possible_negative(self):
        solver = Solver("foo\nbar")
        solver.possible_negatives = "a"
        solver.required_letters = {"a"}
        solver._reconcile_negatives()

        assert len(solver.possible_negatives) == 0
        assert len(solver.negative_letters) == 0
        assert len(solver.required_letters) == 1

    def test_possible_negative_gets_added_to_negative_letters(self):
        solver = Solver("foo\nbar")
        solver.possible_negatives = "a"
        solver._reconcile_negatives()

        assert len(solver.possible_negatives) == 0
        assert len(solver.negative_letters) == 1


class TestFindWords:
    def test_find_words_with_no_pattern_set(self):
        solver = Solver("foo\nbar")
        assert solver.find_words() == ["foo", "bar"]

    def test_find_words_with_all_unknown(self):
        solver = Solver("foo\nbar\nbaz")
        solver.parse_input("gin", "bbb")
        assert solver.pattern == "..."
        assert solver.find_words() == ["foo", "bar", "baz"]

    def test_find_words_with_one_known(self):
        solver = Solver("foo\nbar\nbaz")
        solver.parse_input("gat", "bgb")
        assert solver.pattern == ".a."
        assert solver.find_words() == ["bar", "baz"]

    def test_find_words_with_one_in_wrong_position(self):
        solver = Solver("foo\nbar\nbaz")
        solver.parse_input("dia", "bby")
        assert solver.pattern == "..[^a]"
        assert solver.find_words() == ["bar", "baz"]


class TestParseInput:
    def test_input_with_completely_unknown(self):
        solver = Solver("foo\nbar")
        solver.parse_input("rie", "bbb")
        assert solver.pattern == "..."

    def test_input_with_letter_in_wrong_position(self):
        solver = Solver("foo\nbar")
        solver.parse_input("aft", "ybb")
        assert solver.pattern == "[^a].."
        assert solver.required_letters == {"a"}
        assert solver.not_at_position == ["a", "", "", "", ""]

    def test_input_with_all_known(self):
        solver = Solver("foo\nbar")
        solver.parse_input("foo", "ggg")
        assert solver.pattern == "foo"

    def test_required_and_nap_is_retained(self):
        solver = Solver("foo\nbar\nbaz")
        solver.parse_input("aft", "ybb")
        assert solver.required_letters == {"a"}
        solver.parse_input("pze", "byb")
        assert solver.required_letters == {"a", "z"}
        assert solver.not_at_position == ["a", "z", "", "", ""]


class TestFilterForRequiredAndNegative:
    def test_no_required_or_negative(self):
        solver = Solver("foo\nbar")
        matches = ["foo", "bar"]
        assert solver._filter_for_required_and_negative(matches) == matches

    def test_required_letters_present_in_output(self):
        solver = Solver("foo\nbar")
        matches = ["foo", "bar"]
        solver.required_letters = {"f"}
        assert solver._filter_for_required_and_negative(matches) == ["foo"]

    def test_negative_letters_not_present_in_output(self):
        solver = Solver("foo\nbar")
        matches = ["foo", "bar"]
        solver.negative_letters = {"f"}
        assert solver._filter_for_required_and_negative(matches) == ["bar"]


class TestProcessBlack:
    def test_class_variables_set(self):
        solver = Solver("foo\nbar")
        solver._process_black(2, "a")
        assert "a" in solver.possible_negatives
        assert solver.pattern == "."


class TestProcessYellow:
    def test_class_variables_set(self):
        solver = Solver("foo\nbar")
        solver._process_yellow(2, "a")
        assert "a" in solver.required_letters
        assert "[^a]" in solver.pattern
        assert solver.not_at_position[2] == "a"

        solver._process_yellow(2, "c")
        assert solver.not_at_position[2] == "ac"
        assert "[^ac]" in solver.pattern


class TestProcessGreen:
    def test_class_variables_set(self):
        solver = Solver("foo\nbar")
        solver._process_green(2, "a")
        assert "a" in solver.required_letters
        assert "a" in solver.pattern
        assert solver.at_position[2] == "a"

        solver._process_green(2, "c")
        assert solver.at_position[2] == "a"
