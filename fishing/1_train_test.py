import pandas as pd

inverted = False # Set to True if coordinates are reported as positive in the SW quadrant

kg = pd.read_csv('fishing_result.csv')
thres = pd.read_csv('moving_threshold.csv') #Precomputed moving threshold for each week of the season
lines = pd.read_csv('lines.csv') #Number of lines of each vessel
env = pd.read_csv('environmental.csv') #Created environmental dataset

# Normalize kg to kg/line
kg = pd.merge(kg,lines)
kg.KN = kg.KN/kg.Lineas

# Define productive or unproductive based on the threshold
kg.Day = pd.to_datetime(kg.Day)
kg['Week'] = kg['Day'].dt.isocalendar().week
kg = pd.merge(kg,thres)
kg.KN = kg.KN>kg.Threshold


# Merge environmental
env.Day = pd.to_datetime(env.Day)
data = pd.merge(kg,env)
data = data.dropna()

if inverted:
    kg.Latitude = -1*kg.Latitude
    kg.Longitude = -1*kg.Longitude

data.rename(columns = {'KN':'Tag'}, inplace = True)

# Train/Test split
train = data[data.Day.dt.year!=2022]
test = data[data.Day.dt.year==2022]
train = train.drop(columns=['Embarcacion','Threshold','Day','Lineas'])
test = test.drop(columns=['Embarcacion','Threshold','Day','Lineas'])
test.to_csv('test.csv',index=False)
train.to_csv('train.csv',index=False)