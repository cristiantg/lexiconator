#!/usr/bin/env python3

# Main script.
# This script provides a lexicon file with the following sintax
# <word><tab-symbol><phonetic-transcription> in each line.
# Please run preparing_raw_data.py before to create a suitable
# input file.
# Also please take into account this script outputs entries with
# disambiguation symbols (fast, Kaldi) on duplicate pronunciation
# entries
# Dependencies: CLAM (lm on Ponyland)
# Feel free to change the constants' values in: uber_script.py, local/prepare_lexicon.py and local/join_files.py
# @author Cristian TG
# @since 2021/04/02

import os
import shutil

WEBSERVICES_USERNAME = "CHANGE_VALUE" 
WEBSERVICES_PASSWORD = "CHANGE_VALUE"

# ---------------- OPTION = 1 ----------------
# Just one execution (one folder)
# Just one output lexicon = 1
SUFFIX_OUTPUT_FOLDER = "results"
OPTION = 1


# ---------------- OPTION = 2 ----------------
# N executions (n folders)
# N lexicons, lexicon = 2

# Change these values if you set lexicon = 2:
# Raw input files folder (all of them to be iterated one by one)
RAW_DATA_FOLDER = "raw_input"
# Raw input file folder (just one of them)
RAW_OUTPUT_FOLDER = "raw"


# ---------------- ANY OPTION ----------------
# name+/ Autogenerate files in this folder (you should remove them manually after running this script)
OUTPUT_FOLDER = 'output/'
# name+/ Autogenerate files in this folder
AUX_FOLDER = OUTPUT_FOLDER+'aux/'
# name+/ Autogenerate files in this folder 
DICT_FOLDER = OUTPUT_FOLDER+'dict/'



#########################################################
#########################################################
def main_loop(m_file, aux_file):
  # name+/ Autogenerate files in this folder
  FINAL_FOLDER = OUTPUT_FOLDER+m_file+'-final/'
  if not os.path.exists(FINAL_FOLDER):
    os.makedirs(FINAL_FOLDER)
  # name+/ Autogenerate files in this folder 
  MAPPING_FILE_PATH = FINAL_FOLDER+'mapping.txt'
  open(MAPPING_FILE_PATH, 'w').close()

  if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

  if not os.path.exists(AUX_FOLDER):
    os.makedirs(AUX_FOLDER)
  else:
    os.system('rm -r ' + AUX_FOLDER + '*')

  if not os.path.exists(DICT_FOLDER):
    os.makedirs(DICT_FOLDER)
  else:
    os.system('rm -r ' + DICT_FOLDER + '*')

  print('######## 1/3 ######### python3 local/prepare_lexicon.py', AUX_FOLDER, MAPPING_FILE_PATH)
  os.system('python3 local/prepare_lexicon.py '+AUX_FOLDER + ' ' + MAPPING_FILE_PATH)

  print('######## 2/3 ######### python3 local/g2p_ws.py', WEBSERVICES_USERNAME, "*PASSWORD*", AUX_FOLDER, DICT_FOLDER)
  os.system('python3 local/g2p_ws.py ' + WEBSERVICES_USERNAME + ' ' + WEBSERVICES_PASSWORD + ' ' + AUX_FOLDER + ' ' + DICT_FOLDER)

  print('######## 3/3 ######### python3 local/join_files.py', DICT_FOLDER, FINAL_FOLDER, MAPPING_FILE_PATH)
  os.system('python3 local/join_files.py '+DICT_FOLDER + ' ' + FINAL_FOLDER + ' ' + MAPPING_FILE_PATH)

  if os.path.exists(aux_file):
    os.remove(aux_file)


# OPTION 1: There is prepared an inputFile in input
if OPTION == 1:
  main_loop(SUFFIX_OUTPUT_FOLDER, "")
elif OPTION == 2:
  # OPTION 2: Prepare an inputFile in input
  onlyfiles = [f for f in os.listdir(
      RAW_DATA_FOLDER) if os.path.isfile(os.path.join(RAW_DATA_FOLDER, f))]
  counter = 0
  GITKEEP = ".gitkeep"
  if GITKEEP in onlyfiles:
      onlyfiles.remove(GITKEEP)

  for m_file in onlyfiles:
      counter += 1
      currentFile = RAW_DATA_FOLDER+os.sep+m_file
      print("\nuber: "+RAW_DATA_FOLDER + os.sep+m_file +
            " -> " + str(counter)+"/"+str(len(onlyfiles)))
      aux_file = RAW_OUTPUT_FOLDER+os.sep+m_file
      shutil.copy(currentFile, aux_file)
      print("- copied temporal file in "+aux_file)
      os.system('python3 utils/preparing_raw_data.py '+RAW_OUTPUT_FOLDER)
