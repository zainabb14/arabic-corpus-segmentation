import nltk
import re

def handle_extract_words(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    words = []
    for sentence in sentences:
        tokenized_words = nltk.word_tokenize(sentence)
        cleaned_words = [re.sub(r'[^a-zA-Zء-ي]', '', word) for word in tokenized_words if re.sub(r'[^a-zA-Zء-ي]', '', word)]
        words.extend(cleaned_words)
    return words