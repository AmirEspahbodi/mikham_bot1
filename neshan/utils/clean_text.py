import re
import unicodedata


def cleaning_text(text: str):
    text = text.replace("\u200b", "")
    text = text.replace("\u200c", "")
    text = text.replace("\u200e", "")
    text = re.sub(r"[\u200b\u200c\u200d\u2060\u200e]", "", text)
    text = unicodedata.normalize("NFKC", text)
