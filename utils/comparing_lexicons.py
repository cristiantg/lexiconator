#!/usr/bin/env python3

# Compares two lexicon files providing several stats
# run: python3 comparing_lexicons.py lex1 lex2 1 > out.txt
# example:
# lexi_project=/home/ctejedor/python-scripts/lexiconator
# current_lex=data/local
# python3 $lexi_project/utils/comparing_lexicons.py $current_lex/dict/lexicon.txt $current_lex/dict_test/lexicon.txt 1 > $current_lex/compare.txt
#
# @author Cristian TG
# @since 2021/04/15

import sys
if (len(sys.argv) < 4):
    print("You must add three arguments: the first and second lexicon path and if you want to see a full report (1:yes/0:no).")
    sys.exit(-1)
LEXICON_1 = sys.argv[1]
LEXICON_2 = sys.argv[2]
SHOW_DETAILS = int(sys.argv[3])==1

###############################################################
###############################################################
DISAMBIGUATION_SYMBOL = '#'
def getLexicon(lexicon, path):
    with open(path) as lexi:
        for line in lexi:
            aux = line.split('\t')
            lexicon[aux[0]] = aux[1].replace("\n","").split(" ")
    return lexicon


def getWords(lexicon):
    words = set()
    for word in lexicon:
        words.add(word)
    return words


def getCharacters(lexicon):
    characters = set()
    for word in lexicon:        
        for c in word:
            characters.add(c)
    return characters


def getPhonemes(lexicon):
    phonemes = set()
    disambiguation = set()
    for word in lexicon:
        phones = lexicon[word]
        for p in phones:
            if DISAMBIGUATION_SYMBOL not in p:
                phonemes.add(p)
            else:
                disambiguation.add(p)
    return phonemes, disambiguation



#############################################################
lexicon1 = getLexicon({}, LEXICON_1)
lexicon2 = getLexicon({}, LEXICON_2)

words_l1 = getWords(lexicon1)
words_l2 = getWords(lexicon2)

characters_l1 = getCharacters(lexicon1)
characters_l2 = getCharacters(lexicon2)

phonemes_l1, disambiguation_l1 = getPhonemes(lexicon1)
phonemes_l2, disambiguation_l2 = getPhonemes(lexicon2)


print("\nLEXICON_1", LEXICON_1, "LEXICON_2", LEXICON_2)
print("- Number of words:", len(words_l1),
      len(words_l2), len(words_l1)-len(words_l2))
print("\n- Number of common words:", len(words_l1&words_l2))
if SHOW_DETAILS:
    print(words_l1 & words_l2)
print("- Number of words included in 1 (not in 2):", len(words_l1 - words_l2))
if SHOW_DETAILS:
    print(words_l1 - words_l2)
print("- Number of words included in 2 (not in 1):", len(words_l2 - words_l1))
if SHOW_DETAILS:
    print(words_l2 - words_l1)

print("\n- Number of characters:", len(characters_l1),
      len(characters_l2), len(characters_l1)-len(characters_l2))
print("- Number of common characters:", len(characters_l1 & characters_l2))
if SHOW_DETAILS:
    print(characters_l1 & characters_l2)
print("- Number of characters included in 1 (not in 2):", len(characters_l1 - characters_l2))
if SHOW_DETAILS:
    print(characters_l1 - characters_l2)
print("- Number of characters included in 2 (not in 1):",
      len(characters_l2 - characters_l1))
if SHOW_DETAILS:
    print(characters_l2 - characters_l1)

print("\n- Number of phonemes:", len(phonemes_l1),
      len(phonemes_l2), len(phonemes_l1)-len(phonemes_l2))
print("- Number of common phonemes:", len(phonemes_l1 & phonemes_l2))
if SHOW_DETAILS:
    print(phonemes_l1 & phonemes_l2)
print("- Number of phonemes included in 1 (not in 2):",
      len(phonemes_l1 - phonemes_l2))
if SHOW_DETAILS:
    print(phonemes_l1 - phonemes_l2)
print("- Number of phonemes included in 2 (not in 1):",
      len(phonemes_l2 - phonemes_l1))
if SHOW_DETAILS:
    print(phonemes_l2 - phonemes_l1)

print("\n- Number of disambiguation symbols:", len(disambiguation_l1),
      len(disambiguation_l2), len(disambiguation_l1)-len(disambiguation_l2))
print("- Number of common disambiguation symbols:",
      len(disambiguation_l1 & disambiguation_l2))
if SHOW_DETAILS:
    print(disambiguation_l1 & disambiguation_l2)
print("- Number of disambiguation symbols included in 1 (not in 2):",
      len(disambiguation_l1 - disambiguation_l2))
if SHOW_DETAILS:
    print(disambiguation_l1 - disambiguation_l2)
print("- Number of disambiguation symbols included in 2 (not in 1):",
      len(disambiguation_l2 - disambiguation_l1))
if SHOW_DETAILS:
    print(disambiguation_l2 - disambiguation_l1)
