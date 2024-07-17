import re
import processing.rules as r


def bad_patterns(line, index):  # Cross-check and fix known bad patterns
    mistakes = []
    for word in r.BAD_PATTERNS:
        if word in line:
            mistakes.append(f"Line {index + 1}. {r.BAD_PATTERNS[word]}")
    return mistakes


def comma_after(line, index):  # Check for words that come before a comma
    mistakes = []
    for word in r.COMMA_AFTER:
        if word in line:
            mistakes.append(
                f'Line {index + 1}. Might need a comma after "{word[:-1]}".'
            )
    return mistakes


def phrases_with_very(line, index):  # Check for patterns like "very ..."
    mistakes = []
    for word in r.VERY:
        if word in line:
            mistakes.append(
                f'Line {index + 1}. Consider replacing "{word}" with words like "{r.VERY[word]}" etc'
            )
    return mistakes


def start_with_numbers(line, index):  # Check if a non-empty line starts with a number
    mistakes = []
    if line[0].isdigit():
        mistakes.append(
            f"Line {index + 1}. Avoid starting sentences with numbers. Rewrite by spelling out the number."
        )
    return mistakes


def numbers_next_to_units(line, index):  # Check if units are separated from numbers
    mistakes = []
    for number in range(9):
        for unit in r.UNITS:
            if (
                (f"{number}{unit} " in line)
                or (f"{number}{unit}." in line)
                or (f"{number}{unit}," in line)
            ):
                mistakes.append(
                    f"Line {index + 1}. Put a space between the digit {number} and the unit {unit}"
                )
        if (str(number) + " %" in line) or (str(number) + r" \%" in line):
            mistakes.append(
                f'Line {index + 1}. Percent sign "%" should follow numberals without a space, i.e. {number}%'
            )
    return mistakes


def abbreviations(text):  # Check how many times abbreviations occur in the text
    entire_text = r.unite_valid_lines(text)
    all_abbreviations = re.findall(
        r"\b(?:[A-Z][a-z]?){2,}", entire_text
    )  # Regex to find acronyms/abbreviations
    filtered_abbreviations = []
    for abbreviation in all_abbreviations:
        trimmed_abbreviation = (
            abbreviation[:-1] if abbreviation[-1] == "s" else abbreviation
        )
        filtered_abbreviations.append(trimmed_abbreviation)
    mistakes = []

    # Check how often each abbreviation occurs and comment if less than five
    found_abbreviations = []
    for unique_abbreviation in set(filtered_abbreviations):
        if (
            (unique_abbreviation not in r.ELEMENTS)
            and (unique_abbreviation not in r.EXCEPTIONS)
            and (unique_abbreviation not in r.UNITS)
        ):
            occurance = filtered_abbreviations.count(unique_abbreviation)
            if 0 < occurance < 5:
                found_abbreviations.append(unique_abbreviation)

    # Advise is constructed depending on how many abbreviations were found
    if len(found_abbreviations) == 1:
        mistakes.append(
            f"The abbreviation {found_abbreviations[0]} occurs only a few times. Since abbreviations are hard to decrypt, just spell it out each time. It is easier to read a few words than to search for meanings of abbreviations."
        )
    if len(found_abbreviations) > 1:
        output_string = found_abbreviations[0]
        found_abbreviations[-1] = " and " + found_abbreviations[-1]
        for name in found_abbreviations[1:]:
            output_string += f", {name}"
        mistakes.append(
            f"The abbreviations {output_string} occur only a few times each. Since abbreviations are hard to decrypt, just spell them out each time. It is easier to read a few words than to search for meanings of abbreviations."
        )
    return mistakes


def intro_patterns(text):  # Check for overused introductory phrases
    mistakes = []
    entire_text = r.unite_valid_lines(text)
    for word in r.OVERUSED_INTRO:
        occurance = entire_text.count(word)
        occurance_percentage = occurance / len(entire_text.split(" "))
        if (0.0012 < occurance_percentage < 0.002) and (occurance > 1):
            mistakes.append(
                f'Sentences often start with "{word}". Try alternatives like "{r.OVERUSED_INTRO[word]}".'
            )
        if occurance_percentage > 0.002 and occurance > 1:
            mistakes.append(
                f'Sentences start with "{word}" too often. Try alternatives like "{r.OVERUSED_INTRO[word]}".'
            )
    return mistakes


def redundancy(line, index):  # Check for redundant words
    mistakes = []
    for word in r.REDUNDANT:
        if word in line:
            mistakes.append(
                f'Line {index + 1}. Replace likely redundant "{word}" with just "{r.REDUNDANT[word]}".'
            )
    return mistakes


def negatives(line, index):  # Check for negative words
    mistakes = []
    for word in r.NEGATIVES:
        if word in line:
            mistakes.append(
                f'Line {index + 1}. Replace negative "{word}" with a more positive "{r.NEGATIVES[word]}".'
            )
    return mistakes


def sentence_length(line, index):  # Check if a sentence is too long
    mistakes = []
    sentences = line.split(".")
    if any([len(sentence) > 240 for sentence in sentences]):
        mistakes.append(
            f"Line {index + 1}. The sentence seems to be too long. Consider shortening or splitting it in two."
        )
    return mistakes


def absolutes(line, index):  # Check for absolute wording
    mistakes = []
    for num, word in enumerate(r.ABSOLUTES):
        not_exception = [
            exception not in line for exception in r.ABSOLUTES_EXCEPTIONS[num]
        ]
        if (word in line) and all(not_exception):
            mistakes.append(f"Line {index + 1}. {r.ABSOLUTES[word]}")
    return mistakes


def extreme_quantities(line, index):
    patterns = [
        (
            r"(big|large|small) ((conductivity|conductance|resistance|diffusivity)|(thermal|electrical|interface|boundary) (conductivity|conductance|resistance|resistivity|diffusivity)|frequency|value|temperature|concentration|pressure|altitude)",
            "high/low",
        ),
        (
            r"(big|large|small) (wavelength|lifespan|length|period|time frame|time period|distance|path|mean free path|MFP)",
            "long/short",
        ),
        (r"(big|large|small) (range|spectrum)", "wide/narrow"),
    ]

    mistakes = []
    for pattern, replacement in patterns:
        matches = re.findall(pattern, line)
        mistakes.extend(
            [
                f'Line {index + 1}. Usually "{match[1]}" is {replacement} rather than "{match[0]}".'
            ]
            for match in matches
        )
    return mistakes


def cliches(line, index):  # Check for cliches
    mistakes = []
    for phrase in r.CLICHES:
        if phrase in line:
            mistakes.append(
                f'Line {index + 1}. The phrase "{phrase}" is considered a cliche and should be avoided.'
            )
    return mistakes


def numbers_with_s(line, index):  # Check for number ending with 's
    mistakes = []
    error = re.findall(r"\d's", line)
    if error != []:
        mistakes.append(
            f"Line {index + 1}. Placing 's after a number might be a mistake. For example, these were 2000s with three 0s, and number 0's influence on 2000s' days was clear."
        )
    return mistakes


def difficult_words(text):  # Check for difficult words
    mistakes = []
    found_words = []
    entire_text = r.unite_valid_lines(text)
    for word in r.COMPLEX_WORDS:
        occurance = entire_text.count(word)
        if occurance > 0:
            found_words.append(word)
    if found_words != []:
        synonyms = ""
        errors = ""
        for word in found_words:
            synonyms += '"' + r.COMPLEX_WORDS[word] + '", '
            errors += '"' + word + '", '
        mistakes.append(
            f"You used some difficult words like {errors[:-2]}. Try using simple synonyms, like {synonyms[:-2]} because most readers of scientific papers are not native English speakers."
        )
    return mistakes