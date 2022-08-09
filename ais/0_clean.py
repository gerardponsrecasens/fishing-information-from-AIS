import pandas as pd
import os

############## DATA #################
path = r'path_to_ais_folder'
files = sorted(os.listdir(path))
poteros = pd.read_csv('poteros.csv') #Squid vessels of the Argentina fleet

############ PREPROCESS #############

dataframes = []
for file in files:
    d_path = path+'\\' + file
    data = pd.read_csv(d_path)
    data.columns = ['Vessel Name','IMO','MMSI','Latitude','Longitude','Date','Time','Direction','Degrees','Speed','Position Source']
    data = pd.merge(data,poteros.drop(columns=['IMO','MMSI']))
    data['Day'] = pd.to_datetime(data.Date,format='%d/%m/%Y')
    data['Day'] = data['Day'] + pd.to_timedelta(data.Time)
    data = data.drop(columns=['Direction','Degrees','Position Source','MMSI','Date','Time'])
    data = data[['Vessel Name','Day','Speed','IMO','Latitude','Longitude']]
    data.columns = ['Embarcacion','Fecha','Velocidad','IMO','Latitud','Longitud']
    dataframes.append(data)


data = pd.concat(dataframes)

data.to_csv('ais.csv',index=False)

