import re
from spacy.tokens import Span
from spacy.language import Language
import spacy
from spacy.util import filter_spans
from word2number import w2n


@Language.component("find_numbers")
def find_numbers(doc):
    Span.set_extension("number", default=None, force=True)
    # Basic numbers and tens
    basic_numbers = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen"
    ]

    tens = [
        "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
    ]

    basic_pattern = r"\b(?:" + "|".join(basic_numbers) + r")\b"
    tens_pattern = r"\b(?:" + "|".join(tens) + r")\b"

    # Pattern for numbers up to 99
    up_to_99 = r"(?:" + basic_pattern + r"|" + tens_pattern + r"(?:-" + basic_pattern + r")?)"

    # Pattern for numbers up to 999
    up_to_999 = r"(?:" + basic_pattern + r" hundred(?: and " + up_to_99 + r")?|" + up_to_99 + r")"

    large_numbers = ["thousand", "million", "billion", "trillion", "quadrillion"]

    # Initialize with the basic pattern
    full_pattern = up_to_999

    # Iteratively add larger units
    for large_num in large_numbers:
        full_pattern = r"(?:" + up_to_999 + r" " + large_num + r"(?:, " + up_to_999 + r")?|" + full_pattern + r")"

    def merge_adjacent_matches(matches, original_text):
        merged_matches = []
        i = 0
        while i < len(matches):
            current_match = matches[i]
            span = current_match.span()
            while (i + 1 < len(matches) and 
                   original_text[span[1]:matches[i+1].start()].strip() == "" and 
                   original_text[matches[i+1].start():matches[i+1].end()] == matches[i+1].group()):
                span = (span[0], matches[i+1].end())
                i += 1
            merged_matches.append(span)
            i += 1
        return merged_matches

    matches = list(re.finditer(full_pattern, doc.text.lower()))
    merged_match_spans = merge_adjacent_matches(matches, doc.text.lower())


    new_ents = []
    for start_char, end_char in merged_match_spans:
        # Convert character offsets to token offsets
        start_token = None
        end_token = None
        for token in doc:
            if token.idx == start_char:
                start_token = token.i
            if token.idx + len(token.text) == end_char:
                end_token = token.i
        if start_token is not None and end_token is not None:
            hit_text = doc.text[start_char:end_char]
            hit_num = w2n.word_to_num(hit_text)
            ent = Span(doc, start_token, end_token + 1, label="NUMBER")
            ent._.number = hit_num
            new_ents.append(ent)

    # Combine the new entities with existing entities, ensuring no overlap
    doc.ents = filter_spans(list(doc.ents) + new_ents)
    
    return doc