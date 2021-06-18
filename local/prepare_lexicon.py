#!/usr/bin/env python3

import os
import sys

# Words file with one word in each line, to avoid repeating them in the new lexicon file generated
FINAL_INPUT_FILE = 'input/wordlist'
# Words that will not be included in the final lexicon file. Could be empty
PREVIOUS_WORDS_FILE = ''  # words.txt
# Minimoum lentgh of the final lexicon words 
MIN_LENGTH_OUTPUT_WORDS = 1

# Delete diacritics and other symbols
need_to_clean=True
if need_to_clean:
    print("\t<clean> mode activated")
else:
    print("\t<clean> mode is not activated")
# OPTIONAL
# Be careful, if you want map down digits you need the map_digits_to_words_v2.perl file
# Not included in this repo. due to copyright issues.
DIGITS_TO_WORDS_FILE_PATH = 'local/map_digits_to_words_v2.perl'

OUTPUT_FILE_FOLDER = sys.argv[1]
OUTPUT_FILE_NAME = 'dict-words'
MAPPING_FILE_PATH = sys.argv[2]


if (len(sys.argv) < 3):
    print("You should add two arguments: a folder path for auxiliary files and a path for the mapping file.")
    sys.exit(-1)



########################################################################################
########################################################################################
# You can add/remove as many symbols as you want:
##### "-": " " --> Special case, do not incude it here
REPLACE_SYMBOLS = {"'": "",
                    "\"": "", "\n": "", ";": "",
                   "(": "", ")": "",   ".": "", ":": "", "_": "",
                   "%": "", "•": "", "‘": "", "’": "", "–": "", "[": "", "]": "", 
                   "{": "", "}": "", "<": "", ">": "", "+": "", "=": "", "&": "", 
                   "§": "", "·": "", "*": "", "?": "", "!": "", "#": "", "~": "",
                   "œ": "", "®": "", "…": "", "^": "", "μ": "", "ß": "", "α": "",
                   "β": "", "γ": "", "©": "", "|": ""}
REPLACE_WORDS = {",": "", "/": ""}
NORMALIZE_SYMBOLS = {"Ä": "A", "Ë": "E", "Ï": "I", "Ö": "O", "Ü": "U", "Á": "A", "É": "E",
 "Í": "I", "Ó": "O", "Ú": "U", "À": "A", "È": "E", "Ì": "I", "Ò": "O", "Ù": "U", "ä": "a", 
 "ë": "e", "ï": "i", "ö": "o", "ü": "u", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
 "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u", "å": "a", "Å": "A", "ê": "e", "Ê": "E"}
TEMPORAL_FILE = "tmp"


def map_digits(digits):
    m_text = digits    
    if os.path.isfile(DIGITS_TO_WORDS_FILE_PATH):
        os.system(("echo \"" + m_text + "\"| perl " +
                  DIGITS_TO_WORDS_FILE_PATH + " > "+TEMPORAL_FILE))
        m_text = str(open(TEMPORAL_FILE, 'r').read()).replace('\n', '')
    return m_text
    

def clean_text(originalText):
    for symbol in REPLACE_SYMBOLS:
        originalText = originalText.replace(symbol, REPLACE_SYMBOLS[symbol])
    return originalText


def clean_word(originalWord):
    for symbol in REPLACE_WORDS:
        originalWord = originalWord.replace(symbol, REPLACE_WORDS[symbol])
    return originalWord

## Symbols and numbers
##
def normalizeText(originalText):
    for symbol in NORMALIZE_SYMBOLS:
        originalText = originalText.replace(symbol, NORMALIZE_SYMBOLS[symbol])
    return originalText
    #return ''.join([i for i in originalText if not i.isdigit()])


not_include = set([])
if len(PREVIOUS_WORDS_FILE)>1:
    f = open(PREVIOUS_WORDS_FILE, 'r', encoding='utf8')
    for line in f:
        for word in line.split():
            not_include.add(word.upper())
    f.close()
    print("-> ", len(not_include), "unique words in the <not_include> list")


print("Obtaining/cleaning all words from the source text file...")
words = set([])
cont = 0
f = open(FINAL_INPUT_FILE, 'r', encoding='utf8')
for line in f:
    if need_to_clean:
        line = clean_text(line)
    for word in line.split():
        needs_mapping = False
        if need_to_clean:
            word = normalizeText(clean_word(word))
        if cont%2000==0:
            print(cont, end=' ', flush=True)
        if not (word.isupper()):
            word = word.lower()
        if (len(word) >= MIN_LENGTH_OUTPUT_WORDS) and (word.upper() not in not_include):
            ## 1. Special case - (first and last char)
            if word[0]=='-':
                word = word[1:]
            if (len(word) >= MIN_LENGTH_OUTPUT_WORDS) and (word[-1]=='-'):
                word = word [0:-1]
            # 2. Digits to orthographical transcription
            m_len = len(word)
            if m_len >= MIN_LENGTH_OUTPUT_WORDS:
                current = 0
                aux_word = ''
                aux_char = ''
                aux_digits = ''
                while current < m_len:
                    aux_char = word[current]
                    if aux_char.isdigit():
                        aux_digits+=str(aux_char)
                    else:
                        if len(aux_digits)>0:
                            aux_word+=map_digits(aux_digits)
                            needs_mapping = True
                        aux_digits = ''
                        aux_word+=aux_char
                    current += 1
                if len(aux_digits)>0:
                    aux_word+=map_digits(aux_digits)
                    aux_digits = ''
                    needs_mapping = True
                if needs_mapping:
                    with open(MAPPING_FILE_PATH, 'a') as m_f:
                        m_f.write(aux_word+'\t'+word+'\n')
                words.add(aux_word)
        cont+=1
f.close()
print()
print("-> ", len(words), "unique words")
words = sorted(words)
my_lists = []
list_aux = []
for i in words:
    if len(list_aux) != 0 and len(list_aux) % 100 == 0:
        my_lists.append(list_aux[:])
        list_aux = []
    list_aux.append(i)
my_lists.append(list_aux[:])
print("-> ", len(my_lists), "files")

counter = 0
for l in my_lists:
    counter = counter + len(l)
    with open(OUTPUT_FILE_FOLDER+OUTPUT_FILE_NAME+str(counter)+'.txt', 'w') as f:
        for word in l:
            f.write(word)
            f.write('\n')

if need_to_clean:
    if os.path.isfile(TEMPORAL_FILE):
        os.remove(TEMPORAL_FILE)
