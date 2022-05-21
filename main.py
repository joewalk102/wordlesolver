import re
from pprint import pprint


def parse_input(raw_input):
    unknown_letters = list()
    positioned_letters = ""
    for letter in raw_input.split(" "):
        if "?" in letter:
            unknown_letters.append(str(letter).strip("?"))
            positioned_letters += "."
        else:
            positioned_letters += letter
    return positioned_letters, unknown_letters


def main():
    with open("words.txt", "r") as file:
        words = file.read()
    while True:
        raw_text = input("whatcha got? -> ")
        pattern, unknown = parse_input(raw_text)
        raw_text = input("what's not there? -> ")
        pattern = f"^{pattern}$"
        matches = re.findall(pattern, words, re.M)
        final_matches = list()
        if unknown:
            for m in matches:
                if all([letter in m for letter in unknown]) and not any([letter in m for letter in raw_text]):
                    final_matches.append(m)
        pprint(final_matches)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
