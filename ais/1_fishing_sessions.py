import pandas as pd
from datetime import timedelta
import numpy as np
from geopy import distance


cross_hard = True #Remove rows were vessels are at the harbour.
data = pd.read_csv(r'./ais.csv')




threshold = 1.5  #mph
start = 10 #start of no fishing period
end = 16 #end of no fishing period
radius = 100 #fishing zone outside harbours
consecutive_minutes = 180 #minimum number of consecutive minuts to be considered fishing

data['Fecha'] = pd.to_datetime(data['Fecha']) #CONVERT DATA TO DATETIME FORMAT

#ADD TWO EXTRA COLUMNS:
# - DURATION TILL NEXT TIMESTAMP
# - ARE BOTH TIMESTAMPS ARE GOING IN AN ACCEPTABLE VELOCITY AND ARE INSIDE THE FISHING PERIOD? T/F

data['Duration'] = (data['Fecha'].shift(-1)-data['Fecha']).dt.seconds/60
data['Fishing'] = ((data['Velocidad']<threshold) & (data['Velocidad'].shift(-1)<threshold))*[False if (x.hour+x.minute/60)>start and (x.hour+x.minute/60)<end else True for x  in data['Fecha']]


# WE ASSUME THAT THEY ISSUE THE FISHING REPORT AT THE END, SO THE DAY IN THE PESCA_POTEROS DATASET IS AT THE END OF
# THE FISHING DAY. HENCE, FOR INSTANCE FOR THE DAY 2020-01-12 THE FISHING PERIOD WILL GO FROM 12:00 OF 2020-01-11
# TO 12:00 OF 2020-01-12. WE WILL ADD A NEW COLUMN FOR THE 'ARBITRARY' DAY THEY ARE AT:

data['Day'] = [x if (x.hour+x.minute/60)<12 else x+timedelta(days=1) for x  in data['Fecha']]
data['Day'] = data['Day'].dt.strftime('%Y-%m-%d 00:00:00')

# MAP POSITION TO GRID
data['GridLat'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in data['Latitud']]
data['GridLon'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in data['Longitud']]
data = data[['Embarcacion','Day','Duration','GridLat','GridLon','Fishing']]

# GROUP CONSECUTIVE FISHING PERIODS SO THAT WE GET TOTAL DURATION
data['Diff'] = data[["Embarcacion",'Day','GridLat','GridLon','Fishing']].ne(data[["Embarcacion",'Day','GridLat','GridLon','Fishing']].shift()).any(axis=1).cumsum()
data = data.groupby(['Embarcacion', 'Day','Fishing','Diff','GridLat','GridLon']).sum().reset_index()
data = data.drop(columns=['Diff'])

# REMOVE ROWS WHERE THEY ARE NOT FISHING AND ALSO THE ONES THAT HAVE LOWER DURATION THAN 3 HOURS
data = data[data['Fishing']==True]
data = data[data['Duration']>180]

# REMOVE ROWS WHERE THEY ARE AT HARBOUR
if cross_hard:
    harb = pd.read_csv(r'./included_quadrants.csv')
    harb.columns = ['GridLat','GridLon']
    data = pd.merge(data,harb)

# REMOVE FISHING SESSION TO THE NORTH OF LAT 44 DURING VEDA TIMES
data.Day = pd.to_datetime(data.Day)
d_2016 = data[(data.Day.dt.year==2016)&((data.GridLat < -44) | (data.Day > '2016-04-02'))]
d_2017 = data[(data.Day.dt.year==2017)&((data.GridLat < -44) | (data.Day > '2017-04-07'))]
d_2018 = data[(data.Day.dt.year==2018)&((data.GridLat < -44) | (data.Day > '2018-04-03'))]
d_2019 = data[(data.Day.dt.year==2019)&((data.GridLat < -44) | (data.Day > '2019-04-01'))]
d_2020 = data[(data.Day.dt.year==2020)&((data.GridLat < -44) | (data.Day > '2020-04-01'))]
d_2021 = data[(data.Day.dt.year==2021)&((data.GridLat < -44) | (data.Day > '2021-03-22'))]

data = pd.concat([d_2016,d_2017,d_2018,d_2019,d_2020,d_2021])    

# REMOVE UNWANTED COLUMNS
data = data[['Embarcacion','Day','Duration','GridLat','GridLon']]

# WE SUM DE DURATION GROUPED BY BOAT,DAY AND GRID QUADRANT

duration = data.groupby(['Embarcacion', 'Day','GridLat','GridLon']).sum().reset_index() 
duration['Duration'] = duration['Duration']/60

# WE SUM AS WELL FOR THE TOTAL OF THE DAY, IN ORDER TO COMPUTE THE FRACTION IN EACH QUADRANT
data = data[['Embarcacion','Day','Duration']]
total_duration = data.groupby(['Embarcacion', 'Day']).sum().reset_index() 
total_duration['Duration'] = total_duration['Duration']/60
total_duration.rename(columns={"Duration": "Total_Duration"},inplace=True)

# MERGE THE TWO DURATION DATASETS
duration = pd.merge(duration,total_duration)
duration['Frac'] = duration['Duration']/duration['Total_Duration']
duration = duration.drop(columns=['Total_Duration'])

# SAVE CSV
duration.to_csv(r'./fishing_quadrants.csv',index=False)

