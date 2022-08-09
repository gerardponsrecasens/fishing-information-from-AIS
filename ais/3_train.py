import pandas as pd

data = pd.read_csv(r'tagged.csv')
env = pd.read_csv(r'environmental.csv')

data.Day = pd.to_datetime(data.Day)
env.Day = pd.to_datetime(env.Day)
data = pd.merge(data,env)
data['Week'] = data['Day'].dt.isocalendar().week

data = data.drop(columns=['Day'])

data.to_csv(r'train.csv',index=False)