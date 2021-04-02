#!/usr/bin/env python3

import shutil
import glob
import os
import sys

if (len(sys.argv) < 3):
    print("You should add two arguments: a folder path for retrieving the server data and the output folder")
    sys.exit(-1)


# Personalize the first lines of the final lexicon file
#HEADER = "!SIL\tsil\n<UNK>\tspn\n" # HoMed
HEADER = "<unk>\tunk\n" # JASMIN

FINAL_FOLDER = sys.argv[2]+'final/'
if not os.path.exists(FINAL_FOLDER):
    os.makedirs(FINAL_FOLDER)
AUX_LEXICON_FILE = FINAL_FOLDER+'lexiconordered.pron'
LEXICON_FILE = FINAL_FOLDER+'lexicon.txt'
LOG_FILE = FINAL_FOLDER+'log.txt'




##############################################################
##############################################################
INPUT_EXT = '*.dict'



with open(AUX_LEXICON_FILE, 'wb') as outfile:
    for filename in glob.glob(sys.argv[1]+INPUT_EXT):
        if filename == AUX_LEXICON_FILE:
            # don't want to copy the output into the output
            continue
        with open(filename, 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)

duplicates = []
pron_not_found = []
all_words = set()
with open(AUX_LEXICON_FILE, 'r') as r:
    with open(LEXICON_FILE, 'w') as w:
        w.write(HEADER)        
        for line in sorted(r):
            if "PRONUNCIATION_NOT_FOUND" not in line:
                m_word = str(line.split('\t')[0])
                # To avoid duplicate entries
                if m_word in all_words:
                    duplicates.append(m_word)
                else:
                    w.write(line)
                    all_words.add(m_word)
            else:
                pron_not_found.append(line.replace(
                    "PRONUNCIATION_NOT_FOUND", ""))

os.remove(AUX_LEXICON_FILE)
with open(LOG_FILE, 'w') as w:
    w.write("---- Duplicates:\n")
    for i in duplicates:
        w.write(i+"\n")
    w.write("\n---- PRONUNCIATION_NOT_FOUND:\n")
    for i in pron_not_found:
        w.write(i)

print("\n-> The lexicon file is in:", LEXICON_FILE)
print(str(len(all_words)), "words in the final lexicon file.")

print("\n-> The log file is in:", LOG_FILE)
print("Discarded words:")
print(" "+str(len(duplicates)), "duplicated words.")
print(" "+str(len(pron_not_found)), "words with no pronunciation.\n")
