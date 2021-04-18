#!/usr/bin/env python3

import shutil
import glob
import os
import sys

if (len(sys.argv) < 3):
    print("You should add two arguments: a folder path for retrieving the server data and the output folder for the lexicon")
    sys.exit(-1)

# Personalize the first lines of the final lexicon file
#HEADER = "!SIL\tsil\n<UNK>\tspn\n" # HoMed
HEADER = "<unk>\tunk\n" # JASMIN
# Change this value if you do not want to include disambiguation symbols (Kaldi)
INCLUDE_DISAMBIGUATION_SYMBOLS = True



FINAL_FOLDER = sys.argv[2]
if not os.path.exists(FINAL_FOLDER):
    os.makedirs(FINAL_FOLDER)
AUX_LEXICON_FILE = FINAL_FOLDER+'lexiconordered.pron'
LEXICON_FILE = FINAL_FOLDER+'lexicon.txt'
LOG_FILE = FINAL_FOLDER+'log.txt'
# https://kaldi-asr.org/doc/data_prep.html
# https://kaldi-asr.org/doc/graph.html#graph_disambig
DISAMBIGUATION_SYMBOL = '#'
DISAMBIG_FILE = FINAL_FOLDER+'disambig.txt'
DISAMBIG_DEFAULT_INDEX = 0
SEP_SYMBOL = '\t'
SEP_PHON_SYMBOL = ' '
INPUT_EXT = '*.dict'


##############################################################
##############################################################
with open(AUX_LEXICON_FILE, 'wb') as outfile:
    for filename in glob.glob(sys.argv[1]+INPUT_EXT):
        if filename == AUX_LEXICON_FILE:
            # don't want to copy the output into the output
            continue
        with open(filename, 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)


duplicates = []
pron_duplicates = {}
pron_not_found = []
all_words = set()
all_words_UPPER = set()
all_prons = set()
lexicon = {}
with open(AUX_LEXICON_FILE, 'r') as r:
    for line in sorted(r):
        if "PRONUNCIATION_NOT_FOUND" not in line:
            m_aux = line.split(SEP_SYMBOL)
            m_word = str(m_aux[0])
            m_word_UPPER = m_word.upper()
            m_pron = str(m_aux[1].replace('\n', ''))
            # To avoid duplicated entries
            if (m_word in all_words) or (m_word_UPPER in all_words_UPPER):
                duplicates.append(m_word)
            else:
                all_words.add(m_word)
                all_words_UPPER.add(m_word_UPPER)
                if m_pron in all_prons:
                    pron_duplicates[m_pron] += 1
                else:
                    all_prons.add(m_pron)
                    pron_duplicates[m_pron] = 1
                lexicon[m_word] = [m_pron, int(pron_duplicates[m_pron])]
        else:
            pron_not_found.append(line.replace(
                "PRONUNCIATION_NOT_FOUND", ""))

n_disambig_lines = []
max_disambig_index = DISAMBIG_DEFAULT_INDEX
with open(LEXICON_FILE, 'w') as w:
    w.write(HEADER)
    aux_line = ""
    for m_entry in lexicon:
        m_pron = lexicon[m_entry][0]
        aux_line = m_entry+SEP_SYMBOL+m_pron
        disambig_index = pron_duplicates[m_pron]
        if INCLUDE_DISAMBIGUATION_SYMBOLS and (disambig_index > 1):
            aux_line+= SEP_PHON_SYMBOL+DISAMBIGUATION_SYMBOL+str(lexicon[m_entry][1])
            n_disambig_lines.append(aux_line)
        if disambig_index > max_disambig_index:
            max_disambig_index = disambig_index
        w.write(aux_line + '\n')

if INCLUDE_DISAMBIGUATION_SYMBOLS and (max_disambig_index > DISAMBIG_DEFAULT_INDEX):
    with open(DISAMBIG_FILE, 'w') as w:
        for i in range(DISAMBIG_DEFAULT_INDEX,max_disambig_index+1):
            w.write(DISAMBIGUATION_SYMBOL+str(i)+'\n')

os.remove(AUX_LEXICON_FILE)
with open(LOG_FILE, 'w') as w:
    w.write("---- Duplicates avoided (orthographical transcription): " +
            str(len(duplicates))+" entries:\n")
    for i in duplicates:
        w.write(i+"\n")
    
    if INCLUDE_DISAMBIGUATION_SYMBOLS:
        w.write("---- Disambiguation symbols included in: " +
                str(len(n_disambig_lines))+" entries:\n")
        for i in n_disambig_lines:
            w.write(i+"\n")
    
    w.write("\n---- PRONUNCIATION_NOT_FOUND: " +
                str(len(pron_not_found))+" entries:\n")
    for i in pron_not_found:
        w.write(i)

    w.write("\n-> Disambiguation symbols included in the file "+ DISAMBIG_FILE)
    w.write("\n-> The lexicon file is in: "+LEXICON_FILE)
    w.write("\n"+str(len(all_words)) + " words in the final lexicon file.")

    if INCLUDE_DISAMBIGUATION_SYMBOLS:
        w.write("\n\t- Entries with disambiguation symbols: " +
                str(len(n_disambig_lines))+"\n")
    w.write("\t- Discarded words:\n")
    w.write("\t\t"+str(len(duplicates)) + " duplicated words.\n")
    w.write("\t\t"+str(len(pron_not_found)) + " words with no pronunciation.\n")

print("-> The log file is in: ", LOG_FILE, "\n")
