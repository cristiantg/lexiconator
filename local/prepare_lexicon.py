#!/usr/bin/env python3

import os
import sys

if (len(sys.argv) < 6):
    print("You must add five arguments: a folder path for generating auxiliary files; a path for the mapping file; 0/1 (False/true) for cleaning data: 0/1  (False/true) for leaning diacritics; input/wordlist file path")
    sys.exit(-1)

m_encode = 'utf-8'
#Exception table overruling the output of the g2p. <word><tab><subword1><space><subwordn>. 
# It could be empty
EXCEPTION_TABLE = ''
# Words that will not be included in the final lexicon file.
# It could be empty
PREVIOUS_WORDS_FILE = ''  # words.txt
# Minimum lentgh of the words of the final lexicon  
MIN_LENGTH_OUTPUT_WORDS = 1
# Delete diacritics and other symbols
need_to_clean=sys.argv[3]=='1'
delete_diacritics=sys.argv[4]=='1'
# Words file with one word in each line, to avoid repeating them in the new lexicon file generated
FINAL_INPUT_FILE = sys.argv[5]
# OPTIONAL
# Be careful, if you want map down digits you need the map_digits_to_words_v2.perl file
# Not included in this repo. due to copyright issues.
DIGITS_TO_WORDS_FILE_PATH = 'local/map_digits_to_words_v2.perl'

print("\t<clean> mode activated" if need_to_clean else "\t<clean> mode is not activated")
print("\t<diacritics> will be deleted" if delete_diacritics else "\t<diacritics> will not be deleted")



OUTPUT_FILE_FOLDER = sys.argv[1]
OUTPUT_FILE_NAME = 'dict-words'
MAPPING_FILE_PATH = sys.argv[2]
# Must be the same as in join_files.py
SEP_ISOLATED = '###'
SEP_DIGITS_ISOLATED = '--'

########################################################################################
########################################################################################
# You can add/remove as many symbols as you want:
# Do not include the symbols in DELETE_ONLY_BEGIN_END and in REPLACE_SYMBOLS
# if need_to_clean:
DELETE_ONLY_BEGIN_END = ["-"] ####### You can also add: "\'"
REPLACE_SYMBOLS = {"\"": "", "\n": "", ";": "", "(": "", ")": "", 
                   ".": "", ":": "", "_": "",
                   "%": "", "•": "", "‘": "", "’": "", "–": "", "[": "", "]": "", 
                   "{": "", "}": "", "<": "", ">": "", "+": "", "=": "", "&": "", 
                   "§": "", "·": "", "*": "", "?": "", "!": "", "#": "", "~": "",
                   "œ": "", "®": "", "…": "", "^": "", "μ": "", "ß": "", "α": "",
                   "β": "", "γ": "", "©": "", "|": "", "@": "", "$": ""}
REPLACE_WORDS = {",": "", "/": ""}
NORMALIZE_SYMBOLS = {"Ä": "A", "Ë": "E", "Ï": "I", "Ö": "O", "Ü": "U", "Á": "A", "É": "E",
 "Í": "I", "Ó": "O", "Ú": "U", "À": "A", "È": "E", "Ì": "I", "Ò": "O", "Ù": "U", "ä": "a", 
 "ë": "e", "ï": "i", "ö": "o", "ü": "u", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
 "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u", "å": "a", "Å": "A", "ê": "e", "Ê": "E",
 "â":"a", "ã":"a", "î":"i", "û":"u", "ý":"y", "ÿ":"y", "Â":"A", "Ã":"A", "Î":"I", "Û":"U", 
 "Ý":"Y", "Ÿ":"Y"}
TEMPORAL_FILE = "tmp"


def map_digits(digits):
    m_text = digits    
    if os.path.isfile(DIGITS_TO_WORDS_FILE_PATH):
        os.system(("echo \"" + m_text + "\"| perl " +
                  DIGITS_TO_WORDS_FILE_PATH + " > "+TEMPORAL_FILE))
        m_text = str(open(TEMPORAL_FILE, 'r', encoding=m_encode).read()).replace('\n', '')
    return m_text
    

def clean_text(originalText):
    for symbol in REPLACE_SYMBOLS:
        originalText = originalText.replace(symbol, REPLACE_SYMBOLS[symbol])
    return originalText


def clean_word(originalWord):
    for symbol in REPLACE_WORDS:
        originalWord = originalWord.replace(symbol, REPLACE_WORDS[symbol])
    return originalWord


def normalizeText(originalText):
    for symbol in NORMALIZE_SYMBOLS:
        originalText = originalText.replace(symbol, NORMALIZE_SYMBOLS[symbol])
    return originalText
    #return ''.join([i for i in originalText if not i.isdigit()])

not_include = set([])
if os.path.isfile(PREVIOUS_WORDS_FILE):
    f = open(PREVIOUS_WORDS_FILE, 'r', encoding=m_encode)
    for line in f:
        for word in line.replace('\n','').split():
            not_include.add(word.upper())
    f.close()
    print("\n---> ", len(not_include), "total unique words in the <not_include> list")


exceptions = {}
if os.path.isfile(EXCEPTION_TABLE):
    f = open(EXCEPTION_TABLE, 'r', encoding=m_encode)
    for line in f:
        line_aux = line.replace('\n','').split('\t')
        exceptions[line_aux[0]] = line_aux[1]
    f.close()
    print("\t---> ", len(exceptions), "total words in the exceptions file")


print("\nObtaining/cleaning all words from the source text file...")
original_words = set([])
words = set([])
cont = 0
exception_words = 0
f = open(FINAL_INPUT_FILE, 'r', encoding=m_encode)
for line in f:
    if need_to_clean:
        line = clean_text(line)    
    for word in line.split():
        isolation_subword_count = 0
        needs_isolating = False
        aux_mapping = ''
        if delete_diacritics:
            word = normalizeText(clean_word(word))
        if cont%2000==0:
            print(cont, end=' ', flush=True)
        if not (word.isupper()):
            word = word.lower()
        if (len(word) >= MIN_LENGTH_OUTPUT_WORDS) and (word.upper() not in not_include):
            ## 1. Special cases - (first and last char)
            if need_to_clean:
                for be_symbol in DELETE_ONLY_BEGIN_END:
                    if word[0] == be_symbol:
                        word = word[1:]
                    if (len(word) >= MIN_LENGTH_OUTPUT_WORDS) and (word[-1] == be_symbol):
                        word = word [:-1]

            # 2. Avoiding possible duplicates  
            if word not in original_words:
                original_words.add(word)

                # 3. Exception Table: words already subdivided
                if word in exceptions:
                    aux_pron = exceptions[word]
                    for aux_sub in aux_pron.split(' '):
                        if aux_sub.isdecimal():
                            needs_isolating = True
                            aux_sub = SEP_DIGITS_ISOLATED+map_digits(aux_sub)
                        aux_mapping+=aux_sub
                        words.add(aux_sub+SEP_ISOLATED+str(isolation_subword_count)+SEP_ISOLATED+str(cont)+SEP_ISOLATED)
                        isolation_subword_count+=1
                    exception_words += 1
                else:
                    # 4. Digits to orthographical transcription
                    # 5. Isolate digits from chars to avoid G2P problems
                    m_len = len(word)
                    if m_len >= MIN_LENGTH_OUTPUT_WORDS:
                        current = 0
                        aux_char = ''
                        aux_word = ''                
                        aux_digits = ''

                        while current < m_len:
                            aux_char = word[current]
                            if aux_char.isdigit():
                                needs_isolating = True
                                aux_digits += str(aux_char)
                                if len(aux_word)>0:
                                    iso_word = aux_word+SEP_ISOLATED+str(isolation_subword_count)+SEP_ISOLATED+str(cont)+SEP_ISOLATED 
                                    words.add(iso_word)
                                    aux_mapping+=aux_word
                                    isolation_subword_count+=1
                                    aux_word = ''                        
                            else:
                                aux_word += aux_char
                                if len(aux_digits)>0:
                                    map_word = SEP_DIGITS_ISOLATED+map_digits(aux_digits)
                                    iso_word = map_word+SEP_ISOLATED+str(isolation_subword_count)+SEP_ISOLATED+str(cont)+SEP_ISOLATED 
                                    words.add(iso_word)
                                    aux_mapping+=map_word
                                    isolation_subword_count+=1
                                    aux_digits = ''
                            current += 1
                        # Last cases:
                        if len(aux_word)>0:
                            iso_word = aux_word+SEP_ISOLATED+str(isolation_subword_count)+SEP_ISOLATED+str(cont)+SEP_ISOLATED
                            words.add(iso_word)
                            aux_mapping+=aux_word
                            isolation_subword_count+=1
                            aux_word = ''
                        if len(aux_digits)>0:
                            map_word = SEP_DIGITS_ISOLATED+map_digits(aux_digits)
                            iso_word = map_word+SEP_ISOLATED+str(isolation_subword_count)+SEP_ISOLATED+str(cont)+SEP_ISOLATED
                            words.add(iso_word)
                            aux_mapping+=map_word
                            isolation_subword_count+=1
                            aux_digits = ''

                if needs_isolating and (len(aux_mapping)>0):
                    with open(MAPPING_FILE_PATH, 'a', encoding=m_encode) as m_f:                        
                        m_f.write(aux_mapping+'\t'+word+'\n')
                        needs_isolating = False
                        aux_mapping = ''                        
                cont+=1
f.close()
print()
print("-> ", str(cont), "unique words")
print("-> ", len(words), "subwords (due to isolation)")
#print("-> ", cont, "isolated words")
words = sorted(words)
my_lists = []
list_aux = []
for i in words:
    if len(list_aux) != 0 and len(list_aux) % 100 == 0:
        my_lists.append(list_aux[:])
        list_aux = []
    list_aux.append(i)
my_lists.append(list_aux[:])
print("-> ", len(my_lists), "aux. files to be sent to G2P")

counter = 0
for l in my_lists:
    counter = counter + len(l)
    with open(OUTPUT_FILE_FOLDER+OUTPUT_FILE_NAME+str(counter)+'.txt', 'w', encoding=m_encode) as f:
        for word in l:
            f.write(word)
            f.write('\n')

if os.path.isfile(TEMPORAL_FILE):
    os.remove(TEMPORAL_FILE)
