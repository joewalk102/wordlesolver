import re


def print_grid(words: list, width=5, height=8):
    cursor = 0
    border_len = min(((5 * width) + 8), (len(words) * 7) - 2)
    print("-" * border_len + "\n")
    rows = 1
    while cursor < len(words) and rows < height:
        print("  ".join(words[cursor : cursor + width]), end="\n\n")
        cursor += width
        rows += 1
    print("-" * border_len)


class Solver:
    def __init__(self, words):
        self.words = words
        self.negative_letters = set()
        self.required_letters = set()
        self.not_at_position = [""] * 5
        self.pattern = ""

    def parse_input(self, raw_input):
        self.pattern = ""
        for i, letter in enumerate(raw_input.split(" ")):
            if "?" in letter:
                stripped_letter = str(letter).strip("?")
                if stripped_letter:
                    self.not_at_position[i] += stripped_letter
                    self.required_letters.add(stripped_letter)
                    self.pattern += f"[^{self.not_at_position[i]}]"
                else:
                    self.pattern += "."
            else:
                self.pattern += letter
                self.required_letters.add(letter)

    def add_to_negative(self, new_negatives):
        new_negatives = {
            neg for neg in new_negatives if neg not in self.required_letters
        }
        self.negative_letters = self.negative_letters | new_negatives

    def _filter_for_required_and_negative(self, matches):
        final_matches = list()
        if self.required_letters or self.negative_letters:
            for m in matches:
                if self.required_letters and not all(
                    [letter in m for letter in self.required_letters]
                ):
                    continue
                if self.negative_letters and any(
                    [letter in m for letter in self.negative_letters]
                ):
                    continue
                final_matches.append(m)
        return final_matches or matches

    def find_words(self):
        if not self.pattern:
            return self.words.splitlines()
        matches = re.findall(f"^{self.pattern}$", self.words, flags=re.M)
        return self._filter_for_required_and_negative(matches)


def main():
    with open("words.txt", "r") as file:
        words = file.read()
    go_again = True
    solver = Solver(words=words)
    while go_again:
        raw_text = input("whatcha got? -> ")
        # Expected pattern (separated by spaces):
        # "?" for unknown letter (black)
        # "?l" for unknown position (yellow)
        # "l" for known letter and position (green)
        solver.parse_input(raw_text)

        print("Current omitted letters: " + " ".join(solver.negative_letters))
        # Expected: All black letters with no spaces.
        solver.add_to_negative(input("what's not there? -> "))

        print_grid(solver.find_words()[:40])

        go_again = input("go again? (y/n) -> ").lower().strip() == "y"


if __name__ == "__main__":
    try:
        main()
        print("\n--END OF LINE--")
    except KeyboardInterrupt:
        pass
