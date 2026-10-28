"""
FixMyText AI — Text preprocessing pipeline.

Used by both training scripts and the live classifier.
Preserves negation words (not, never, no) while cleaning.
"""

import re


# Words that carry important meaning for classification
_NEGATION_WORDS = {"not", "no", "never", "nor", "none", "nothing", "nowhere",
                   "neither", "nobody", "hardly", "barely", "scarcely",
                   "doesn", "dont", "doesnt", "didnt", "cant", "cannot",
                   "wont", "wouldnt", "shouldnt", "isnt", "arent", "wasnt",
                   "werent", "hasnt", "havent", "hadnt"}

_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such",
    "only", "own", "same", "so", "than", "too", "very", "just", "about",
    "up", "down", "and", "but", "or", "if", "while", "because", "until",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "am",
}


def normalize_text(text: str) -> str:
    """Lowercase, strip URLs, remove non-alphanumeric chars, collapse whitespace."""
    text = (text or "").lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(text: str, keep_negation: bool = True) -> str:
    """Remove common English stop words, optionally preserving negation."""
    tokens = text.split()
    stop = _STOPWORDS - _NEGATION_WORDS if keep_negation else _STOPWORDS
    return " ".join(w for w in tokens if w not in stop)


def preprocess(text: str, remove_stops: bool = False) -> str:
    """Full preprocessing pipeline used before model input."""
    text = normalize_text(text)
    if remove_stops:
        text = remove_stopwords(text, keep_negation=True)
    return text
