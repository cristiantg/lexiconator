#!/usr/bin/env python3

# Main script
# Dependencies: CLAM (lm on Ponyland)
# Feel free to change the constants' values in: uber_script.py, local/prepare_lexicon.py and local/join_files.py
# @author Cristian TG
# @since 2021/04/02

import os

WEBSERVICES_USERNAME = "CHANGE_VALUE"
WEBSERVICES_PASSWORD = "CHANGE_VALUE"

# name+/ Autogenerate files in this folder (you should remove them manually after running this script)
OUTPUT_FOLDER = 'output/'
# name+/ Autogenerate files in this folder
AUX_FOLDER = OUTPUT_FOLDER+'aux/'
# name+/ Autogenerate files in this folder 
DICT_FOLDER = OUTPUT_FOLDER+'dict/'




#########################################################
#########################################################
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


print('######## 1/3 ######### python3 local/prepare_lexicon.py', AUX_FOLDER)
os.system('python3 local/prepare_lexicon.py '+AUX_FOLDER)

print('######## 2/3 ######### python3 local/g2p_ws.py',
      WEBSERVICES_USERNAME, "*PASSWORD*", AUX_FOLDER, DICT_FOLDER)
os.system('python3 local/g2p_ws.py ' + WEBSERVICES_USERNAME + ' ' +
          WEBSERVICES_PASSWORD + ' ' + AUX_FOLDER + ' ' + DICT_FOLDER)

print('######## 3/3 ######### python3 local/join_files.py', DICT_FOLDER, OUTPUT_FOLDER)
os.system('python3 local/join_files.py '+DICT_FOLDER + ' ' + OUTPUT_FOLDER)
