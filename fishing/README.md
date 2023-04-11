Instructions of how to preprocess the fishing data. ***This part should be done after running the code in the AIS folder***.

- **0-CLEAN**: Given all the fishing reports by the company, we obtain the quantities fishedn by each boat in a day by executing the code 0_clean_reports.py Moreover if the locations contains missing values, they are imputed aswell.
*¡¡¡Some reports contain typos in the location (e.g. 5º57' when it should be 53º57'), which should be solved manually by looking the last reported location for the same boat!!!*

	Input: fishing reports .csv file| fishing_locations .csv file

	Output: fishing_results.csv (file containg the Vessel,Day,Location and Kg)

  

- **1-TRAIN/TEST**: The reports are tagged according to the their productiveness. To do so, the fished quantity is first normalized by the number of lines of the boat, and then compared against a dynamic threshold. Then, the environmental information is added, and finally the train/test splits are created based on their year.

	Input: environmental.csv | lines.csv | moving_threshold.csv | fishing_results.csv

	Output: train.csv | test.csv

![Figure7](https://user-images.githubusercontent.com/95172600/231098220-a26c6097-b7f7-4e6b-bb62-165f40a30d4d.jpg)
