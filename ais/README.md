Different preprocessing steps with AIS data

  

- **0-CLEAN**: First of all, with the 0_clean.py script, the squid vessels are selected and the data is cleaned/preprocessed.

	Input: .csv raw AIS files

	Output: Clean .csv AIS file

  

- **1-FISHING SESSIONS**: Use the heuristic rules to detect when squid vessels are fishing, using the script 1_fishing_sessions.py

	Input: Clean .csv AIS file

	Output: .csv file with the detected fishing sessions, along with their duration

  

- **2-TAGGING**: Use heuristic rules to tag the fishing sessions as productive/non-productive, using the script 2_tagging.py

	Input: fishing_sessions.csv file

	Output: tagged .csv file

  

- **3-TRAIN SET:** Add environmental variables to the tagged file

	Input: tagged.csv | environmental.csv

	Output: train.csv
