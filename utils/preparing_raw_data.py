#!/usr/bin/env python3

# Prepare a single text file with one word in each line from 
# x raw text files in a specific folder
# @author Cristian TG
# @since 2021/04/02

# Please change the value of these variables:
RAW_DATA_FOLDER = "raw"
FINAL_INPUT_FOLDER = "input/"
FINAL_INPUT_FILE = FINAL_INPUT_FOLDER+"wordlist"


###############################################################
###############################################################
import os
if not os.path.exists(FINAL_INPUT_FOLDER):
    os.makedirs(FINAL_INPUT_FOLDER)

onlyfiles = [f for f in os.listdir(
    RAW_DATA_FOLDER) if os.path.isfile(os.path.join(RAW_DATA_FOLDER, f))]

wordlist = set()
for m_file in onlyfiles:
    with open(RAW_DATA_FOLDER+os.sep+m_file) as f:
        for line in f:    
            for m_word in line.split():
                wordlist.add(m_word)

wordlist = sorted(wordlist, key=lambda v: (v.upper(), v[0].islower()))
with open(FINAL_INPUT_FILE, "w") as f:
    for word in wordlist:
        f.write(word+"\n")
print("Created input file in "+FINAL_INPUT_FILE)
