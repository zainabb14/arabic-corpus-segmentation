from .get_affixes import get_affixes

valid_prefixes = ['ال', 'ب', 'ك', 'ل', 'و', 'س', 'ف', 'ت', 'أ']
valid_suffixes = ['ه', 'ها', 'ك', 'ي', 'نا', 'كم', 'كن', 'هم', 'هن', 'ت', 'ون', 'ين', 'ات', 'ة']


def analyze_segmentation(camel_segmentation, pyaramorph_segmentation):
    camel_affixes = get_affixes(camel_segmentation)
    pyaramorph_affixes = get_affixes(pyaramorph_segmentation)

    camel_confidence = 1
    pyaramorph_confidence = 1

    camel_prefix_matches = sum(1 for prefix in camel_affixes['prefixes'] if prefix in valid_prefixes)
    camel_suffix_matches = sum(1 for suffix in camel_affixes['suffixes'] if suffix in valid_suffixes)
    camel_affixes_count = len(camel_affixes['prefixes']) + len(camel_affixes['suffixes'])
    camel_matches = camel_prefix_matches + camel_suffix_matches
    if camel_matches == camel_affixes_count:
        camel_confidence += 1
    else:
        camel_confidence -= 1

    pyaramorph_prefix_matches = sum(1 for prefix in pyaramorph_affixes['prefixes'] if prefix in valid_prefixes)
    pyaramorph_suffix_matches = sum(1 for suffix in pyaramorph_affixes['suffixes'] if suffix in valid_suffixes)
    pyaramorph_affixes_count = len(pyaramorph_affixes['prefixes']) + len(pyaramorph_affixes['suffixes'])
    pyaramorph_matches = pyaramorph_prefix_matches + pyaramorph_suffix_matches
    if pyaramorph_matches == pyaramorph_affixes_count:
        pyaramorph_confidence += 1
    else:
        pyaramorph_confidence -= 1

    camel_stem = camel_affixes['stem']
    pyaramorph_stem = pyaramorph_affixes['stem']

    if len(camel_stem) >= 3:
        camel_confidence += 1
    elif camel_stem in valid_suffixes:
        camel_confidence += 1
    else:
        camel_confidence -= 1

    if len(pyaramorph_stem) >= 3:
        pyaramorph_confidence += 1
    elif pyaramorph_stem in valid_suffixes:
        pyaramorph_confidence += 1
    else:
        pyaramorph_confidence -= 1

    return camel_confidence, pyaramorph_confidence
