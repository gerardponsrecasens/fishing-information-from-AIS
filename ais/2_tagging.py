import pandas as pd
import numpy as np
from datetime import timedelta

df = pd.read_csv('fishing_quadrants.csv')
df = df.dropna()
df.Day = pd.to_datetime(df.Day)
df = df.sort_values(by=['Embarcacion','Day'])


n = len(df)

# RULES BASED ON SATYING IN THE SAME FISHING POSITION
tag_1 = np.zeros(n)
for i in range(n-1):
    j = 1
    while (i+j)<n and df.iloc[i,1] == df.iloc[i+j,1]: #In case it has moved in the same day
        j +=1
    
    # When they change of location
    if (i+j)<n and (df.iloc[i,0] == df.iloc[i+j,0]) and (df.iloc[i,2] != df.iloc[i+j,2] or df.iloc[i,3] != df.iloc[i+j,3]) and (df.iloc[i+j,1] == df.iloc[i,1]+timedelta(1)) :
        # If they stayed in that quadrant for more than one day:
        lat = df.iloc[i+j,2]
        lon = df.iloc[i+j,3]
        
        k = 1
        while ((i+j+k)<(n)) and (df.iloc[i+j,1] == df.iloc[i+j+k,1]): #In case it has moved in the same day
             k+=1
        if (i+j+k<n) and (df.iloc[i+j,0]==df.iloc[i+j+k,0]) and (lat==df.iloc[i+j+k,2]) and (lon==df.iloc[i+j+k,3]):
            #Good Position
            tag_1[i+j]=1
        elif (i+j+k>=n):
            pass
        else:
            #Bad Position
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
        df_following = df[(df.Embarcacion!=ship)&(df.GridLat==lat)&(df.GridLon==lon)&(df.Day==day+timedelta(1))]
        
        #There where boats in the grid, and they are still there:
        if len(df_day)!=0 and len(df_following)!=0:
            tag_2.append(1) #Good Old Grid
        # There where boats in the gris, and they also left
        elif len(df_day)!=0 and len(df_following)==0:
            tag_2.append(-1) #Bad Old Grid
        else:
            tag_2.append(0)
    else:
        tag_2.append(0)
                    
tag_2.append(0)


# Create the tags
df['tag2'] = tag_2
df['tag1'] = tag_1
df['Tag'] = df['tag1']+df['tag2']
df = df.drop(columns=['tag1','tag2','Frac','Duration','Embarcacion'])
df = df.groupby(['Day','GridLat','GridLon']).sum().reset_index()
df = df[df['Tag']!=0]
df.Tag = [True if x>0 else False for x in df.Tag]

# Store
df.columns = ['Day','Latitude','Longitude','Tag']
df.to_csv('tagged.csv',index=False)