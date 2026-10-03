import re


def is_arabic(text):
    arabic_char_range = set(range(0x0600, 0x06FF + 1)) | set(range(0x0750, 0x077F + 1)) | set(
        range(0x08A0, 0x08FF + 1)) | set(range(0xFB50, 0xFDFF + 1)) | set(range(0xFE70, 0xFEFF + 1))
    return all(ord(char) in arabic_char_range or char.isspace() for char in text)


def get_affixes(word):
    parts = word.split()

    if len(parts) == 1:
        return {
            "prefixes": [],
            "suffixes": [],
            "stem": parts[0],
        }

    affixes = {
        "prefixes": [],
        "suffixes": [],
        "stem": "",
    }
    found = False
    for i, part in enumerate(parts):
        if len(part) >= 3:
            affixes["stem"] = part
            found = True
        elif len(part) < 3 and not found:
            affixes["prefixes"].append(part)
        elif len(part) < 3 and found:
            affixes["suffixes"].append(part)

    return affixes
