import re
from collections import defaultdict


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
        self.at_position = [""] * 5
        self.pattern = ""
        self.possible_negatives = ""

        self.color_router = {
            "g": self._process_green,
            "y": self._process_yellow,
            "b": self._process_black,
        }

    def _process_green(self, location, letter):
        self.pattern += letter
        if self.at_position[location]:
            return
        self.required_letters.add(letter)
        self.at_position[location] = letter

    def _process_yellow(self, location, letter):
        self.not_at_position[location] += letter
        self.required_letters.add(letter)
        self.pattern += f"[^{self.not_at_position[location]}]"

    def _process_black(self, location, letter):
        self.pattern += "."
        self.possible_negatives += letter

    def _reconcile_negatives(self):
        new_negatives = {
            neg for neg in self.possible_negatives if neg not in self.required_letters
        }
        self.negative_letters = self.negative_letters | new_negatives
        self.possible_negatives = ""

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

    def parse_input(self, raw_input, colors):
        self.pattern = ""
        for i in range(len(raw_input)):
            if colors[i] in self.color_router:
                self.color_router[colors[i]](i, raw_input[i])
                self._reconcile_negatives()
            else:
                print("Unexpected input in colors. Please try again.")
                break

    def find_words(self):
        if not self.pattern:
            return self.words.splitlines()
        matches = re.findall(f"^{self.pattern}$", self.words, flags=re.M)
        return self._filter_for_required_and_negative(matches)


    def get_common_letters(self, words):
        letters = defaultdict(lambda : 0)
        # Get the occurrence of all letters in all words in the word list
        # and record them in a dict where the letter is the key and the
        # occurrence is the val.
        for word in words:
            for letter in word:
                if letter not in self.negative_letters:
                    letters[letter] += 1
        return letters

    def get_suggested_words(self, words, common_letters):
        # Sort the letters by highest occurrence.
        top_common = set(
            [k for k, v in sorted(common_letters.items(), key=lambda item: item[1], reverse=True)][:6]
        )
        print(f"top_common: {top_common}")
        word_freq = dict()
        # Find the number of letters in each word that matches
        # the top common occurrences and put into a dictionary with
        # the word as the key and the number of letters that occur
        # in top common in the value.
        for word in words:
            num_common_letters = len([letter for letter in word if letter in top_common])
            num_unique_letters = len(set(word))
            word_freq[word] = min([num_common_letters, num_unique_letters])
        # Sort the words by the highest number of letters in common.
        return [k for k, v in sorted(word_freq.items(), key=lambda item: item[1], reverse=True)]


def _input_correct_length(prompt, input_length):
    """
    loop to ensure the length of the guess is correct.
    """
    while True:
        value = input(prompt)
        if len(value) == input_length:
            return value


def main():
    with open("words.txt", "r") as file:
        words = file.read()
    solver = Solver(words=words)
    while True:
        raw_text = _input_correct_length("what's your guess? -> ", 5)
        colors = _input_correct_length("what were the colors? -> ", 5).strip().lower()
        solver.parse_input(raw_text, colors)
        words = solver.find_words()

        print("Suggestions by word frequency:")
        print_grid(words[:40])

        common_letters = solver.get_common_letters(words)
        suggested_words = solver.get_suggested_words(words, common_letters)

        print("Suggestions by letter frequency:")
        print_grid(suggested_words)


if __name__ == "__main__":
    try:
        main()
        print("\n--END OF LINE--")
    except KeyboardInterrupt:
        pass
