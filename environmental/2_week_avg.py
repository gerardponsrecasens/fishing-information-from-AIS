import pandas as pd
from datetime import timedelta

######### CHLOROPHYLL #########
env = pd.read_csv(r'chlorophyll.csv')
env = env.sort_values(by=['Longitude','Latitude','Day'])
env['Day'] = pd.to_datetime(env['Day'])

n = len(env)

week = []
for i in range(n):
    temporal = []
    lat = env.iloc[i,1]
    lon = env.iloc[i,2]
    time = env.iloc[i,0]
    for shift in range(1,8):
        if (i-shift) >=0 and env.iloc[i-shift,1]==lat and env.iloc[i-shift,2]==lon and env.iloc[i,4] != 'Missing' and (env.iloc[i-shift,0]+timedelta(days=shift))==time:
            temporal.append(env.iloc[i-shift,3])
    if len(temporal)>0:
        week.append(sum(temporal)/len(temporal))
    else:
        week.append('')


env['CWeekAvg'] = week

env.to_csv(r'chl_week.csv',index=False)



######### TEMPERATURE #########
env = pd.read_csv(r'temperature.csv')
env = env.sort_values(by=['Longitude','Latitude','Day'])
env['Day'] = pd.to_datetime(env['Day'])

n = len(env)

week = []
for i in range(n):
    temporal = []
    lat = env.iloc[i,1]
    lon = env.iloc[i,2]
    time = env.iloc[i,0]
    for shift in range(1,8):
        if (i-shift) >=0 and env.iloc[i-shift,1]==lat and env.iloc[i-shift,2]==lon and env.iloc[i,4] != 'Missing' and (env.iloc[i-shift,0]+timedelta(days=shift))==time:
            temporal.append(env.iloc[i-shift,3])
    if len(temporal)>0:
        week.append(sum(temporal)/len(temporal))
    else:
        week.append('')


env['TWeekAvg'] = week

env.to_csv(r'temp_week.csv',index=False)



######### SLA #########
env = pd.read_csv(r'sla.csv')
env = env.sort_values(by=['Longitude','Latitude','Day'])
env['Day'] = pd.to_datetime(env['Day'])
env['SLA'] = pd.to_numeric(env['SLA'])

n = len(env)


week = []
for i in range(n):
    temporal = []
    lat = env.iloc[i,1]
    lon = env.iloc[i,2]
    time = env.iloc[i,0]
    for shift in range(1,8):
        if (i-shift) >=0 and env.iloc[i-shift,1]==lat and env.iloc[i-shift,2]==lon and (env.iloc[i-shift,0]+timedelta(days=shift))==time and env.iloc[i-shift,3] != 99 :
            temporal.append(env.iloc[i-shift,3])
    if len(temporal)>0:
        week.append(sum(temporal)/len(temporal))
    else:
        week.append('')


env['SWeekAvg'] = week

env.to_csv(r'sla_week.csv',index=False)



import pandas as pd
from datetime import timedelta

########## WIND #########
env = pd.read_csv(r'wind.csv')
env = env.sort_values(by=['Longitude','Latitude','Day'])
env['Day'] = pd.to_datetime(env['Day'])

n = len(env)

week = []
for i in range(n):
    temporal = []
    lat = env.iloc[i,1]
    lon = env.iloc[i,2]
    time = env.iloc[i,0]
    for shift in range(1,8):
        if (i-shift) >=0 and env.iloc[i-shift,1]==lat and env.iloc[i-shift,2]==lon and env.iloc[i,4] != 'Missing' and (env.iloc[i-shift,0]+timedelta(days=shift))==time:
            temporal.append(env.iloc[i-shift,3])
    if len(temporal)>0:
        week.append(sum(temporal)/len(temporal))
    else:
        week.append('')


env['WWeekAvg'] = week

env.to_csv(r'wind_week.csv',index=False)

