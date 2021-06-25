# lexiconator
Creates a single file (lexicon format: word /tab-symbol/  phones) from a list of text files using the [G2P](https://webservices.cls.ru.nl/g2pservice/index/) webservice of CLST, Dutch CGN2 (under [CLAM](https://proycon.github.io/LaMachine/) environment and Python3).



## 1. Prepare input data and values of variables
1. The `utils/preparing_raw_data.py` script will extract all words possible from specific text files. You just need to put as many text files as you want under one folder: `utils/preparing_raw_data.py#RAW_DATA_FOLDER`.
 
1. The generated file `utils/preparing_raw_data.py#FINAL_INPUT_FILE` in `utils/preparing_raw_data.py#FINAL_INPUT_FOLDER` will be used as input for the next step.

1.  `uber_script.py`:
*Mandatory*: `WEBSERVICES_USERNAME`, `WEBSERVICES_PASSWORD`, `OPTION`,
*Optional*: `OUTPUT_FOLDER`, `AUX_FOLDER`, `DICT_FOLDER`, `SUFFIX_OUTPUT_FOLDER`, `RAW_DATA_FOLDER`, `RAW_OUTPUT_FOLDER`

1.  `local/prepare_lexicon.py`:
*Mandatory*: `FINAL_INPUT_FILE` (must be the same as `utils/preparing_raw_data.py#FINAL_INPUT_FILE`)
*Optional*: `EXCEPTION_TABLE`, `PREVIOUS_WORDS_FILE`, `need_to_clean`, `DIGITS_TO_WORDS_FILE_PATH` (.perl file not included in this repo. due to copyright, please contact me to access this file. You could also delete its use in the code).

1. `local/join_files.py`:
*Mandatory*: `HEADER`, `INCLUDE_DISAMBIGUATION_SYMBOLS`
*Optional*: `FINAL_FOLDER`, `LEXICON_FILE`, `AUX_LEXICON_FILE`, `LOG_FILE`


**Important**: phonetic transcription of numbers are not supported by the current G2P service. You may (a) use their orthographical word representation with a .perl script `local/prepare_lexicon.py#DIGITS_TO_WORDS_FILE_PATH` and `local/prepare_lexicon.py#need_to_clean=True`, (b) do it by yourself or (c) just ignore them.



## 2. How to run this project
**PART 1: Preparing raw data as input**
1. Put your text files into the path: `utils/preparing_raw_data.py#RAW_DATA_FOLDER`
1. Run `python3 utils/preparing_raw_data.py`

**PART 2: Obtaining the lexicon file**
1. Make sure you have set the values of the *Mandatory* variables of the scripts. Also set `OPTION=1` on `uber_script.py`
1. (On Ponyland): Log into one of the [servers](https://ponyland.science.ru.nl/doku.php?id=wiki:ponyland:about): `ssh rarity`
1. Activate your LaMachine: `lm` or `lamachine-lacristianmachine-activate` (replace `lacristianmachine` for the name of your LaMachine).
1. Run `python3 uber_script.py`


## 3. Results
The final lexicon file will be under the path set in the variable: `local/join_files.py#FINAL_FOLDER`


## 4. Extra utilities
1. You can use the `utils/extracting_words.py` script to obtain all words from files in a folder (with or without digits) and specifying the word separator in those files.

1. You can also use the `utils/comparing_lexicons.py` script to compare two lexicon files (Kaldi format) in terms of words, characters and phones.

1. You can also use the `utils/extract_ortho.py` script to obtain the orthographical transcription of the lexicon files.


## 5. Contact
Cristian Tejedor-García
Email: cristian [dot] tejedorgarcia [at] ru [dot] nl