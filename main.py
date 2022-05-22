import re
from pprint import pprint


def parse_input(raw_input):
    unknown_letters = list()
    positioned_letters = ""
    for letter in raw_input.split(" "):
        if "?" in letter:
            stripped_letter = str(letter).strip("?")
            if stripped_letter:
                unknown_letters.append(stripped_letter)
                positioned_letters += f"[^{stripped_letter}]"
            else:
                positioned_letters += "."
        else:
            positioned_letters += letter
    return positioned_letters, unknown_letters


def main():
    with open("words.txt", "r") as file:
        words = file.read()
    go_again = True
    negative_letters = ""
    while go_again:
        raw_text = input("whatcha got? -> ")
        pattern, unknown = parse_input(raw_text)
        print("Current omitted letters: " + negative_letters)
        negative_letters += input("what's not there? -> ")
        pattern = f"^{pattern}$"
        matches = re.findall(pattern, words, re.M)
        final_matches = list()
        if unknown:
            for m in matches:
                if all([letter in m for letter in unknown]) and not any([letter in m for letter in negative_letters]):
                    final_matches.append(m)
        pprint(final_matches)
        go_again = input("go again? (y/n) -> ").lower().strip() == "y"


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
