#!/usr/bin/env python3

# Extracts the orthographical representation of the words of the
# lexicon files (Kaldi format)
# @author Cristian TG
# @since 2021/04/18

# Please change the value of these variables:
LEXICON_FOLDER = "compare/lexicons"
ORTHO_FOLDER = "compare/ortho"


###############################################################
###############################################################
import os

onlyfiles = [f for f in os.listdir(
    LEXICON_FOLDER) if os.path.isfile(os.path.join(LEXICON_FOLDER, f))]

for m_file in onlyfiles:
    currentFile = LEXICON_FOLDER+os.sep+m_file
    words = []
    with open(currentFile) as f:
        for line in f:
            ortho = line.split("\t")[0]
            words.append(ortho)
    with open(ORTHO_FOLDER+os.sep+m_file,"w") as w:
        for word in words:
            w.write(word+"\n")
