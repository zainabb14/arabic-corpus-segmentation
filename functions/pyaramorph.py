import pyaramorph
import re

# Initialize the AraMorph analyzer
analyzer = pyaramorph.Analyzer()


def process_string(s):
    # Remove the 'pos: ' prefix
    s = s.replace("pos: ", "")

    # Split by '+' and process each part
    parts = s.split("+")
    results = []
    for part in parts:
        # Split by '/' and take the first part
        subpart = part.split("/")[0]
        results.append(subpart)

    # Concatenate the results with '+'
    result_string = "+".join(results)
    return result_string


def remove_diacritics(text):
    # Remove diacritics (Tashkeel) using regex
    return re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)


def pyaramorph_segment(words):
    segmented_words = []
    for word in words:
        # Analyze the word
        results = analyzer.analyze_text(word)
        resultFinal = ""
        # Process the analysis results
        for result in results:
            for analysis in result:
                if len(analysis.split("\n")) == 4:
                    resultFinal = pyaramorph.buckwalter.buck2uni(process_string(analysis.split("\n")[1]))
        result_final = remove_diacritics(resultFinal.replace('+', ' '))
        result_final = result_final.replace('+', ' ').strip()
        result_final = re.sub(r'\s+', ' ', result_final)

        segmented_words.append(' '.join(result_final.split()))
    return segmented_words