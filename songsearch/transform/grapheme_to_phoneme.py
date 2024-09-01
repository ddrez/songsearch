from metaphone import doublemetaphone
from anyascii import anyascii 

def convert_g2p(
    grapheme: str,
) -> str:
    translit = anyascii(grapheme)
    return doublemetaphone(translit)[0]
