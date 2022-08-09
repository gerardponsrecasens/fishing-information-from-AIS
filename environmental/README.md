
Explanation of how to process the environmental variables:

  

- **DOWNLOAD** : First of all, the different environmental variables need to be dowloaded via API (or other prefered procedure) and stored locally.

  

- **0-REESCALE** : Then, depending on the files and variables, the 0_reescale.R code should be used appropiately, to obtain a folder per variable,with all the .nc files converted to 0.5ºx0.5º scale.

	Input: original .nc files

	Output: reescaled .nc files

  

- **1-MISSING VALUES AND CSV**: The different environmental files .nc are converted to .csv format and the missing values are also addressed. These procedures are done using the 1_*.py codes. Hence, a csv file is obtained for each variable, with missing values imputed. Moreover, if the environmental files contain data for irrrelevant parts of the globe (i.e. not EEZ), they are filtered out.
*¡¡¡ The folder should contain files for all days, without temporal gaps. If gaps are present, the code should be runed onces for every consecutive temporal sequence!!!*

  

	Input: reescaled .nc files | 1a_coordinates.csv

	Output: .csv files with imputed missing values

  

- **2-WEEK AVERAGE**: The different environmental.csv files need to be averaged by week, as it is the input the model expects. As before, it must be executed once per file, in case of temporal gaps. The code for this step is 2_week_avg.py

	Input: .csv daily environmental files

	Output: .csv weekly environmental files

  

- **3-CHL LAG**: Compute the 11 weeks chlorophyll-a lag, using the script 3_chl_lag.py.

	Input: .csv daily chlorophyll file.

	Output: .csv file with the lag values.

  

- **4-JOIN**: The weekly averages and the chl-a lag ara joined by day and grid.

	Input: weekly .csv files | lag .csv file

	Output: final environmental .csv file