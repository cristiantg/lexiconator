#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Filters to clean and normalize words for preparing a lexicon files.
# Recommended order of use for Kaldi 'text' file: 
# remove_begin_end(normalize_text(clean_word(clean_text(text), '<unk>'), True), 1)
# Recommended order of use for Kaldi 'lexicon' file: 
# replace_word(remove_begin_end(normalize_text(clean_word(clean_text(text), ''), True), 1))
'''

# You can add/remove as many symbols as you want:
# Do not include the symbols in DELETE_ONLY_BEGIN_END and in REPLACE_SYMBOLS
DELETE_ONLY_BEGIN_END = ["-"] ####### You can also add: "\'"

REPLACE_AMPERSAND=' -en- ' # Exactly like this because of the G2P tool
# Do not include "&", since it will be considered as "en"
REPLACE_SYMBOLS = {"\"": "", "\n": "", ";": "", "(": "", ")": "", 
                   ".": "", ":": "", "_": "",
                   "%": "", "•": "", "‘": "", "’": "", "–": "", "[": "", "]": "", 
                   "{": "", "}": "", "<": "", ">": "", "+": "", "=": "",
                   "§": "", "·": "", "*": "", "?": "", "!": "", "#": "", "~": "",
                   "œ": "", "®": "", "…": "", "^": "", "μ": "", "ß": "", "α": "",
                   "β": "", "γ": "", "©": "", "|": "", "@": "", "$": "",
                   u'\u200b':"", u'\u200c':""}
REPLACE_XXX = '' # You could set this value to: <unk>
# Do not include xxx in REPLACE_WORDS, just set the value in REPLACE_XXX
REPLACE_WORDS = {",": "", "/": "", "SIL": ""}
NORMALIZE_SYMBOLS = {"Ä": "A", "Ë": "E", "Ï": "I", "Ö": "O", "Ü": "U", "Á": "A", "É": "E",
 "Í": "I", "Ó": "O", "Ú": "U", "À": "A", "È": "E", "Ì": "I", "Ò": "O", "Ù": "U", "ä": "a", 
 "ë": "e", "ï": "i", "ö": "o", "ü": "u", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
 "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u", "å": "a", "Å": "A", "ê": "e", "Ê": "E",
 "â":"a", "ã":"a", "î":"i", "û":"u", "ý":"y", "ÿ":"y", "Â":"A", "Ã":"A", "Î":"I", "Û":"U", 
 "Ý":"Y", "Ÿ":"Y"}
# Common replacements for Dutch transcriptions of exact words (not parts of the word)
NORMALIZE_SECOND_ROUND={"okee": "ok", "oke": "ok", "okey": "ok", "OKEE": "ok", "OKE": "ok",
 "OKEY": "ok", "MIJN": "mijn", "mn":"mijn", "m'n": "mijn", "M'N": "mijn", "mjn": "mijn",
  "'t":"het", "'T":"het", "t":"het", "'n": "een", "Een":"een", "EEN":"een", "z'n":"zijn", "zn":"z'n",
   "d'r":"daar", "dr":"daar",
   "'s":"s", "zo'n":"zoon",
   "'k":"ik","'K":"ik",
   "uh": ""}

# Recommended: 1 step
def clean_text(text, keepUnk=False):
    TEMP_SUB = 'AABCDEFGHIJKLMNOPQRSTUWXYZZ' if keepUnk else ''      
    if '<unk>' in text or '<UNK>'in text:
        text = text.replace('<unk>',TEMP_SUB).replace('<UNK>',TEMP_SUB)
    for symbol in REPLACE_SYMBOLS:      
        text = text.replace(symbol, REPLACE_SYMBOLS[symbol])
    if keepUnk:
        text = text.replace(TEMP_SUB,'<unk>')
    return text

# Recommended: 2 step
def clean_word(word, xxx=REPLACE_XXX):
    for symbol in REPLACE_WORDS:
        word = word.replace(symbol, REPLACE_WORDS[symbol])
    return word.replace('xxx', xxx)

# Recommended: 3 step
def normalize_text(text, delDiacritics=True):
    if delDiacritics:
        for symbol in NORMALIZE_SYMBOLS:
            text = text.replace(symbol, NORMALIZE_SYMBOLS[symbol])
    if not (text.isupper()):
        text = text.lower()
    return text.replace('&',REPLACE_AMPERSAND)

# Recommended: 4 step
def remove_begin_end(word, MIN_LENGTH_OUTPUT_WORDS):    
    if len(word)>=MIN_LENGTH_OUTPUT_WORDS:
        for be_symbol in DELETE_ONLY_BEGIN_END:
            if word[0] == be_symbol:
                word = word[1:]
            if (len(word) >= MIN_LENGTH_OUTPUT_WORDS) and (word[-1] == be_symbol):
                word = word [:-1]
    return word

# Recommended: 5 step
def replace_word(word, delDiacritics=True):
    if delDiacritics:
        for symbol in NORMALIZE_SECOND_ROUND:
            if len(symbol)==len(word):
                word = word.replace(symbol, NORMALIZE_SECOND_ROUND[symbol])
    return word