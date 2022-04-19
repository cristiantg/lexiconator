#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil
import glob
import os
import sys

if (len(sys.argv) < 5):
    print("You must add four arguments: a folder path for retrieving the server data, the output folder for the lexicon; a path for the mapping file; and the header file for the lexicon file.")
    sys.exit(-1)

REPLACE_AMPERSAND=' -en- ' # Exactly like this
m_encode = 'utf-8'
SEP_SYMBOL = '\t'
#HEADER = "!SIL\tsil\n<UNK>\tspn\n" # Personalize the first lines of the final lexicon file
HEADER = sys.argv[4].replace('<TAB>', SEP_SYMBOL)
# Change this value whether you want or not to include disambiguation symbols (Kaldi)
INCLUDE_DISAMBIGUATION_SYMBOLS = False

PRONUN_NOT_FOUND='PRONUNCIATION_NOT_FOUND'
MAPPING_FILE_PATH = sys.argv[3]
FINAL_FOLDER = sys.argv[2]
AUX_LEXICON_FILE = os.path.join(FINAL_FOLDER,'lexiconordered.pron')
LEXICON_FILE = os.path.join(FINAL_FOLDER,'lexicon.txt')
LOG_FILE =  os.path.join(FINAL_FOLDER,'log.txt')
# https://kaldi-asr.org/doc/data_prep.html
# https://kaldi-asr.org/doc/graph.html#graph_disambig
DISAMBIGUATION_SYMBOL = '#'
DISAMBIG_FILE = os.path.join(FINAL_FOLDER,'disambig.txt')
DISAMBIG_DEFAULT_INDEX = 0
SEP_PHON_SYMBOL = ' '
INPUT_EXT = '*.dict'
# Must be the same as in prepare_lexicon.py
SEP_ISOLATED = '###'


##############################################################
##############################################################
with open(AUX_LEXICON_FILE, 'wb') as outfile:
    for filename in glob.glob(sys.argv[1]+INPUT_EXT):
        if filename == AUX_LEXICON_FILE:
            # don't want to copy the output into the output
            continue
        with open(filename, 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)


mapping_words = {}
with open(MAPPING_FILE_PATH, 'r', encoding=m_encode) as m_f:
    for line in m_f:
        if len(line)>0:
            aux = line.replace('\n','').split('\t')
            mapping_words[aux[0]] = aux[1]


# 1. obtain all subwords and words
pron_not_found = []
aux_lexicon_entries = {}
with open(AUX_LEXICON_FILE, 'r', encoding=m_encode) as r:
    for line in sorted(r):
        #if PRONUN_NOT_FOUND not in line:
        line=line.replace(PRONUN_NOT_FOUND, "")
        line=line.replace(REPLACE_AMPERSAND,'&')
        m_aux = line.split(SEP_SYMBOL)
        m_word = str(m_aux[0])
        m_pron = str(m_aux[1].replace('\n', ''))
                       
        aux_word = m_word.split(SEP_ISOLATED)
        _word_id = aux_word[-2]
        _subword_id = aux_word[-3]
        _word_text = aux_word[0]
        if _word_id in aux_lexicon_entries:
            aux_lexicon_entries[_word_id].append((_subword_id, _word_text, m_pron))
        else:
            aux_lexicon_entries[_word_id] = [(_subword_id, _word_text, m_pron)]
        #else:
        #    pron_not_found.append(line.replace(
        #        PRONUN_NOT_FOUND, ""))

# 1.1 Check if there are any entries with no phonetic transcription at all:
temporal_aux = {}
for ent in aux_lexicon_entries:
    phon_trans=''
    for subelem in aux_lexicon_entries[ent]:
        phon_trans+=subelem[2]
    if len(phon_trans)!=0:
        temporal_aux[ent]=aux_lexicon_entries[ent]
aux_lexicon_entries=temporal_aux

# 2. Create a new list of all words obtained by the G2P (possible duplicates)
isolated_words = []
for m_id in aux_lexicon_entries:
    aux_subwords = sorted(aux_lexicon_entries[m_id], key=lambda x: x[0])
    aux_unzip = list(zip(*aux_subwords))
    isolated_words.append(((''.join(aux_unzip[1])), (' '.join(aux_unzip[2]))))

# 3. Final filter: no duplicates
duplicates = []
pron_duplicates = {}
all_words = set()
all_words_UPPER = set()
all_prons = set()
lexicon = {}
for m_entry in isolated_words:
    # To avoid duplicated entries
    m_word = m_entry[0].replace(REPLACE_AMPERSAND,'&')
    m_pron = m_entry[1]              
    m_word_UPPER = m_word.upper()
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
        
        lexicon[m_word if m_word not in mapping_words else mapping_words[m_word]] = [m_pron, int(pron_duplicates[m_pron])]


# 4. Generating the final lexicon file
n_disambig_lines = []
max_disambig_index = DISAMBIG_DEFAULT_INDEX
with open(LEXICON_FILE, 'w', encoding=m_encode) as w:
    w.write(HEADER+'\n')
    aux_line = ""
    for m_entry in sorted(lexicon):
        m_entry = m_entry.replace(REPLACE_AMPERSAND,'&')
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
    with open(DISAMBIG_FILE, 'w', encoding=m_encode) as w:
        for i in range(DISAMBIG_DEFAULT_INDEX,max_disambig_index+1):
            w.write(DISAMBIGUATION_SYMBOL+str(i)+'\n')

os.remove(AUX_LEXICON_FILE)


####################### 5. LOG
with open(LOG_FILE, 'w', encoding=m_encode) as w:
    w.write("The lexicon file is on: "+LEXICON_FILE)
    w.write("\n"+str(len(all_words)) + " words in the final lexicon file.\n")  
    w.write("\n---- Duplicates avoided (orthographical transcription): " +
            str(len(duplicates))+" entries:\n")
    for i in duplicates:
        w.write(i+"\n")
    
    w.write("\n---- Words with digits (mapping file): " +
            str(len(mapping_words))+"\n")
        
    for i in sorted(mapping_words):
        w.write(mapping_words[i]+" "+i+"\n")

    if INCLUDE_DISAMBIGUATION_SYMBOLS:
        w.write("\n---- Disambiguation symbols included in: " +
                str(len(n_disambig_lines))+" entries:\n")
        for i in n_disambig_lines:
            w.write(i+"\n")
    
    w.write("\n---- "+PRONUN_NOT_FOUND+": " +
                str(len(pron_not_found))+" entries:\n")
    for i in pron_not_found:
        w.write(i)      

    if INCLUDE_DISAMBIGUATION_SYMBOLS:
        w.write("\n-> Disambiguation symbols included in the file "+ DISAMBIG_FILE)
        w.write("\n\t- Entries with disambiguation symbols: " +
                str(len(n_disambig_lines))+"\n")
    w.write("\n- Discarded words:\n")
    w.write("\t"+str(len(pron_not_found)) + " words with no pronunciation.\n")

print("-> The lexicon file:", LEXICON_FILE)
print("\t-> Number of entries:", len(all_words))
print("-> The log file:", LOG_FILE)
print("-> The mapping file: ", MAPPING_FILE_PATH)