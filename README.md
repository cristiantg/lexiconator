# lexiconator
Creates a single file (lexicon format: <word><separator-symbol><phones>) from a list of text files using the [G2P](https://webservices.cls.ru.nl/g2pservice/index/) webservice of CLST, Dutch CGN2 (under [CLAM](https://proycon.github.io/LaMachine/) environment and Python3).


## 1. How to run this project
1. (On Ponyland): Log into one of the [servers](https://ponyland.science.ru.nl/doku.php?id=wiki:ponyland:about): `ssh rarity`
1. Activate your LaMachine: `lm` or `lamachine-lacristianmachine-activate` (replace `lacristianmachine` for the name of your LaMachine).
1. Move to this project's folder: `m_project=/home/ctejedor/python-scripts/lexiconator && cd $m_project`


**STEP 1: Preparing raw data as input**
1. Place all your text files into the same path: `cp <files> <path_to_txt_files>`
1. Run `python3 $m_project/utils/preparing_raw_data.py <path_to_txt_files> $m_project/input`

**STEP 2: Obtaining the lexicon file**
1. Set `OPTION=1` on `uber_script.py`.
1. Run `python3 $m_project/uber_script.py <WEBSERVICES_USERNAME> <WEBSERVICES_PASSWORD> $m_project 1 1 "<unk><TAB>spn" $m_project/input/wordlist $m_project/output`


## 2. Results
The final lexicon file will be under the path: `$m_project/output`


## 3. Prepare input data and values of variables
1. The `utils/preparing_raw_data.py` script will extract all words possible from specific text files. You just need to put as many text files as you want under one folder specified as an argument: `utils/preparing_raw_data.py#RAW_DATA_FOLDER` and the output folder `utils/preparing_raw_data.py#FINAL_INPUT_FOLDER`.
 
1. The generated file `utils/preparing_raw_data.py#FINAL_INPUT_FILE` in `utils/preparing_raw_data.py#FINAL_INPUT_FOLDER` will be used as input for the next step.

1.  `uber_script.py`:
*Mandatory parameters*: `$WEBSERVICES_USER`, `$WEBSERVICES_PASSWORD`, `$lexi_project_PATH`, `$CLEAN (0-1)`, `$DIACRITICS (0-1)`, `$HEADER_LEXICON`, `$FINAL_INPUT_FILE`, 
*Optional*: `OPTION`, `OUTPUT_FOLDER`, `AUX_FOLDER`, `DICT_FOLDER`, `SUFFIX_OUTPUT_FOLDER`, `RAW_DATA_FOLDER`, `RAW_OUTPUT_FOLDER`

1.  `local/prepare_lexicon.py`:
*Mandatory parameters*: `$AUX_FOLDER`, `$MAPPING_FILE_PATH`, `$CLEAN`, `$DIACRITICS`, `$FINAL_INPUT_FILE` (must be the same as `utils/preparing_raw_data.py#FINAL_INPUT_FILE`)
*Optional*: `EXCEPTION_TABLE`, `PREVIOUS_WORDS_FILE`, `DIGITS_TO_WORDS_FILE_PATH` (.perl file not included in this repo. due to copyright, please contact me to access this file. You could also delete its use in the code).

1. `local/join_files.py`:
*Mandatory parameters*: `DICT_FOLDER`, `FINAL_FOLDER`, `MAPPING_FILE_PATH`, `HEADER`
*Optional*: `INCLUDE_DISAMBIGUATION_SYMBOLS`, `LEXICON_FILE`, `AUX_LEXICON_FILE`, `LOG_FILE`


**Important**: phonetic transcription of numbers are not supported by the current G2P service. You may (a) use their orthographical word representation with a .perl script `local/prepare_lexicon.py#DIGITS_TO_WORDS_FILE_PATH` and `local/prepare_lexicon.py#need_to_clean=True`, (b) do it by yourself or (c) just ignore them.


## 4. Extra utilities
1. You can use the `utils/extracting_words.py` script to obtain all words from files in a folder (with or without digits) and specifying the word separator in those files.

1. You can also use the `utils/comparing_lexicons.py` script to compare two lexicon files (Kaldi format) in terms of words, characters and phones.

1. You can also use the `utils/extract_ortho.py` script to obtain the orthographical transcription of the lexicon files.


## 5. Contact
Cristian Tejedor-García
Email: cristian [dot] tejedorgarcia [at] ru [dot] nl