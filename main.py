from processing.general import *
from processing.contrary import *

def main(text):
    results = []

    # General checks:
    results += intro_patterns(text)
    results += abbreviations(text)
    results += difficult_words(text)

    for index, line in enumerate(text):
        results += bad_patterns(line, index)
        results += start_with_numbers(line, index)
        results += phrases_with_very(line, index)
        results += comma_after(line, index)
        results += numbers_next_to_units(line, index)
        results += redundancy(line, index)
        results += negatives(line, index)
        results += absolutes(line, index)
        results += sentence_length(line, index)
        results += cliches(line, index)
        results += numbers_with_s(line, index)
        results += extreme_quantities(line, index)

    if len(results) == 0:
        results = ["Looks like a great memo!"]
    return results


if __name__ == "__main__":
    path = "memo.txt"
    with open(path, "r") as manuscript:
        text = manuscript.readlines()
    results = main(text)
    for line in results:
        print(line + "\n")