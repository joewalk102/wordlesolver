import re
from pprint import pprint

class Solver:
    def __init__(self, words):
        self.words = words
        self.negative_letters = set()
        self.required_letters = list()
        self.not_at_position = [""] * 5
        self.pattern = ""

    def parse_input(self, raw_input):
        self.pattern = ""
        for i, letter in enumerate(raw_input.split(" ")):
            if "?" in letter:
                stripped_letter = str(letter).strip("?")
                if stripped_letter:
                    self.not_at_position[i] += stripped_letter
                    self.required_letters.append(stripped_letter)
                    self.pattern += f"[^{self.not_at_position[i]}]"
                else:
                    self.pattern += "."
            else:
                self.pattern += letter

    def add_to_negative(self, new_negatives):
        self.negative_letters = self.negative_letters | set(new_negatives)

    def find_words(self):
        if not self.pattern:
            return self.words.splitlines()
        matches = re.findall(f"^{self.pattern}$", self.words, flags=re.M)
        if self.required_letters or self.negative_letters:
            final_matches = list()
            for m in matches:
                if self.required_letters and not all([letter in m for letter in self.required_letters]):
                    continue
                if self.negative_letters and any([letter in m for letter in self.negative_letters]):
                    continue
                final_matches.append(m)
            return final_matches
        return matches


def main():
    with open("words.txt", "r") as file:
        words = file.read()
    go_again = True
    solver = Solver(words=words)
    while go_again:
        raw_text = input("whatcha got? -> ")
        solver.parse_input(raw_text)

        print("Current omitted letters: " + " ".join(solver.negative_letters))
        solver.add_to_negative(input("what's not there? -> "))

        pprint(solver.find_words())

        go_again = input("go again? (y/n) -> ").lower().strip() == "y"


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
