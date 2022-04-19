#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Removes the id column of Kaldi text files.
# INPUT format: ID<space>sentence
# OUTPUT format: sentence

for m_file in ['list_of_kaldi_text_files']:
    textForLM=m_file+'_.txt'
    all_lines = []
    #print(m_file)
    with open(m_file) as f:
        for line in f:
            all_lines.append(line.replace("\n","").split(" ")[1:])
    with open(textForLM, "w") as f:
        for line in all_lines:
            f.write(" ".join(line)+"\n")
    print("Created specific "+textForLM+" file")
