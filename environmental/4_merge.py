import pandas as pd
from datetime import datetime, timedelta
## Read files
temp = pd.read_csv(r'./temp_week.csv')
temp.Day = pd.to_datetime(temp.Day)
chlor = pd.read_csv(r'./chlor_week.csv')
chlor.Day = pd.to_datetime(chlor.Day)
bath = pd.read_csv(r'./bathymetry.csv')
temp.Day = pd.to_datetime(temp.Day)
wind = pd.read_csv(r'./wind_week.csv')
wind.Day = pd.to_datetime(wind.Day)
sla = pd.read_csv(r'./sla_week.csv')
sla.Day = pd.to_datetime(sla.Day)
lag = pd.read_csv(r'./lag.csv')
lag.Day = pd.to_datetime(lag.Day)
lag = lag.drop(columns=['Chlorophyll','ChlorOrigin','grid'])

#Create day file
start = datetime(2017,1,1)
days = 365*5 + 1 #2020 is a leap year
day_list = []
for i in range(days):
    day_list.append(start)
    start += timedelta(days=1)
day = pd.DataFrame(day_list,columns=['Day'])
day.Day = pd.to_datetime(day.Day)


all = pd.merge(day,bath,how='cross')
all = pd.merge(all,temp)
all = pd.merge(all,chlor)
all = pd.merge(all,wind)
all = pd.merge(all,sla)
all = pd.merge(all,lag)
all.to_csv(r'./environmental.csv',index=False)

