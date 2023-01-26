#!/usr/bin/env python3

# Extracts the orthographical representation of the words of a
# single lexicon files (Kaldi format)
# @author Cristian TG
# @since 2023/01/26

import sys
if (len(sys.argv) < 3):
    print("You should add two arguments: the lexicon file path and the output file path")
    sys.exit(-1)

LEXICON_FILE = sys.argv[1]
ORTHO_OUTPUT_FILE = sys.argv[2]


###############################################################
###############################################################
import os

words = []
with open(LEXICON_FILE, encoding='utf-8') as f:
    for line in f:
        ortho = line.split("\t")[0]
        words.append(ortho)
with open(ORTHO_OUTPUT_FILE,"w", encoding='utf-8') as w:
    for word in words:
        w.write(word+"\n")
