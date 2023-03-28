import pandas as pd
import numpy as np
from datetime import timedelta

df = pd.read_csv('fishing_quadrants.csv')
df = df.dropna()
df.Day = pd.to_datetime(df.Day)
df = df.sort_values(by=['Embarcacion','Day'])

na = 2 #Number of additonal days other vessels need to fish in a quadrant after the studies vessel moves, to consider that a bad movement -> productive quadrant
nc = 2 #Number of consecutive days a vessel fishes in a quadrant after it moves there, to be considered a productive quadrant

n = len(df)
# Rules based on staying in the same position after moving, for nc days

# We tag as: 1 productive, -1 negative, 0 noninformative
tag_1 = np.zeros(n)

for i in range(n-1): #We know that the last day in the dataset is not useful
    
    # In case in the day of study it has already moved to other positions: check if next records are from the same day and boat
    j = 1
    while (i+j)<n and df.iloc[i,1] == df.iloc[i+j,1]: 
        j +=1
    
    # When they change of location: the next record is for the same boat, in a different location and with a lapse of 1 or two days
    if (i+j)<n and (df.iloc[i,0] == df.iloc[i+j,0]) and (df.iloc[i,2] != df.iloc[i+j,2] or df.iloc[i,3] != df.iloc[i+j,3]) and ((df.iloc[i+j,1] == df.iloc[i,1]+timedelta(1)) or (df.iloc[i+j,1] == df.iloc[i,1]+timedelta(2))):
        
        # Look if at the nc day is still there and fishing:
        lat = df.iloc[i+j,2]
        lon = df.iloc[i+j,3]
        day = df.iloc[i+j,1] + timedelta(nc -1)
        emb = df.iloc[i+j,0]
        
        if len(df[(df['Day']==day)&(df['GridLat']==lat)&(df['GridLon']==lon)&(df['Embarcacion']==emb)])==1:
            tag_1[i+j]=1
        else:
            tag_1[i+j]=-1


# RULES BASED ON OTHER VESSELS BEHAVIOUR
tag_2 = []
for i in range(n-1):
    ship = df.iloc[i,0]
    lat = df.iloc[i,2]
    lon = df.iloc[i,3]
    day =  df.iloc[i,1]
    
    j = 1
    while (i+j)<n and df.iloc[i,1] == df.iloc[i+j,1]: #In case it has moved in the same day
        j +=1
    
    # If they have moved to another quadrant
    if (i+j)<n and (df.iloc[i,0] == df.iloc[i+j,0]) and (df.iloc[i,2] != df.iloc[i+j,2] or df.iloc[i,3] != df.iloc[i+j,3]) and (df.iloc[i+j,1] == df.iloc[i,1]+timedelta(1)) :
        df_day = df[(df.Embarcacion!=ship)&(df.GridLat==lat)&(df.GridLon==lon)&(df.Day==day)]
        
        

        following = True
        for k in range(na):
            df_following = df[(df.Embarcacion!=ship)&(df.GridLat==lat)&(df.GridLon==lon)&(df.Day==day+timedelta(k+1))]
            if len(df_following==0):
                following = False
        #There where boats in the grid, and they are still there:
        if len(df_day)!=0 and following:
            tag_2.append(1) #Good Old Grid
        # There where boats in the grid, and they also left
        elif len(df_day)!=0 and not following:
            tag_2.append(-1) #Bad Old Grid
        else:
            tag_2.append(0)
    else:
        tag_2.append(0)
                    
tag_2.append(0)


# Create the tags
if len(tag_1)==len(tag_2):
    df['tag2'] = tag_2
    df['tag1'] = tag_1
    df['Tag'] = df['tag1']+df['tag2']
    df = df.drop(columns=['tag1','tag2','Frac','Duration','Embarcacion'])
    df = df.groupby(['Day','GridLat','GridLon']).sum().reset_index()
    df = df[df['Tag']!=0]
    df.Tag = [True if x>0 else False for x in df.Tag]

# Store
df = df.drop_duplicates()
df.columns = ['Day','Latitude','Longitude','Tag']