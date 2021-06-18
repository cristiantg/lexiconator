#!/usr/bin/env python3

# Extracts words from all texts in a folder
# Input: UTF-8 files. Please make sure your files are in UTF-8.
# Output: files with the words extracted from each file
# @author Cristian TG
# @since 2021/04/15

# Please change the value of these variables:
WORD_SEPARATOR = " "
RAW_DATA_FOLDER = "raw/lexicons_2"
RAW_DATA_REPLACEMENTS = {"<": " ", ">": " ", "\t": " ", "$": " ", "=\"":" "}
FINAL_INPUT_FOLDER = "raw_input/"
EXTENSION_TO_EXTRACT = ".txt"
EXTENSION_OUTPUT = ""
KEEP_DIGITS = True

FINAL_INPUT_FILE = FINAL_INPUT_FOLDER+"_"


###############################################################
###############################################################
import os
if not os.path.exists(FINAL_INPUT_FOLDER):
    os.makedirs(FINAL_INPUT_FOLDER)

onlyfiles = [f for f in os.listdir(
    RAW_DATA_FOLDER) if os.path.isfile(os.path.join(RAW_DATA_FOLDER, f))]

count = 0
for m_file in onlyfiles:
    wordlist = set()
    currentFile = RAW_DATA_FOLDER+os.sep+m_file
    if currentFile.endswith(EXTENSION_TO_EXTRACT):
        count += 1
        with open(currentFile) as f:            
            for line in f:
                for key in RAW_DATA_REPLACEMENTS:
                    line = line.replace(key, RAW_DATA_REPLACEMENTS[key])
                for m_word in line.split(WORD_SEPARATOR):
                    wordlist.add(m_word)

        # Problems with some files:
        # wordlist = sorted(wordlist, key=lambda v: (v.upper(), v[0].islower()))
        wordlist = sorted(wordlist)
        finalName = FINAL_INPUT_FILE+m_file+EXTENSION_OUTPUT
        with open(finalName, "w") as f:
            for word in wordlist:
                word = word.strip()
                if not KEEP_DIGITS:                    
                    word = ''.join([i for i in word if not i.isdigit()])
                if len(word)>0:
                    f.write(word+"\n")
        print("Created input file in "+finalName)
print(str(count)+" files processed")
