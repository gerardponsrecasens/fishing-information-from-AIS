import os
import netCDF4 as nc4
import numpy as np
import pandas as pd
import csv
from datetime import datetime, timedelta

############# COORDINATES OF THE WANTED POINTS #####################

coords = pd.read_csv(r'.\1a_coordinates.csv')
points_lat = coords['Latitud'].to_numpy()
points_lon =  coords['Longitud'].to_numpy()
points = []
for i,j in zip(points_lat,points_lon):
    points.append([i,j])

############################ CSV ##################################

output_file = r'.\temperature.csv'
with open(output_file, 'a', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(['Day','Latitude','Longitude','Temperature','TempOrigin'])

######################## DATA ##########################################

path_cd = r'path_to_temp_folder'
cd_files = sorted(os.listdir(path_cd)) #Sort to ensure order by day


############################# INDEX ###################################
# The inout grid has a spacing of 0.5 and covers the whole globe (90 to -90, -180 to 180)

grid = 0.5
index_cd = []
for point in points:
    latitude = point[0]
    longitude = point[1]
    ilat = int(abs(np.floor((90-latitude)/grid)))
    ilon = int(abs((-180-longitude)/grid))
    index_cd.append([ilat,ilon])


############################ PREPROCESS ############################

start = 0
end = len(cd_files)-1

date = datetime(2017,1,1) #Date of the first file
weights = {1:3,2:2,3:1} #Weight given to previous/future days when imputing the missing values

for i in range (end+1):

    temp = [] #List of final temperatures for each grid for the day
    agg = [] #List of aggregated temperatures, for imputing missing values
    possible = [] #Days used to perform the imputation

    if i-3>= start:
        possible.extend([i-1,i-2,i-3])
    elif i-2>=start:
        possible.extend([i-1,i-2])
    elif i-1>=start:
        possible.append(i-1)
    
    if i+3<=end:
        possible.extend([i+1,i+2,i+3])
    elif i+2<=end:
        possible.extend([i+1,i+2])
    elif i+1<=end:
        possible.append(i+1)

    
    df_cd = nc4.Dataset(path_cd+'\\'+cd_files[i])
    cd_actual = df_cd['sea_surface_temperature'][:,:]

    week_data = {}
    for j in possible:
        df_week = nc4.Dataset(path_cd+'\\'+cd_files[j])
        week_data[j]=df_week['sea_surface_temperature'][:,:]

    for pos in index_cd:
        if cd_actual.mask[pos[0],pos[1]] == False:
            temp.append(cd_actual[pos[0],pos[1]])
            agg.append('Actual')
        else:
            week = []
            pond=[]
            for j in possible:
                c = week_data[j]
                if c.mask[pos[0],pos[1]] == False:
                    week.append(c[pos[0],pos[1]])
                    pond.append(weights[int(np.absolute(i-j))])
            if len(week) != 0:
                num = 0
                den = 0
                for cc,ww in zip(week,pond):
                    num += cc*ww
                    den += ww
                temp.append(num/den)
                agg.append('Aggregated')
            else: 
                temp.append('')
                agg.append('Missing') 

    with open(output_file, 'a', newline="", encoding='UTF8') as f:
        writer = csv.writer(f)
        for c,p,a in zip(temp,points,agg):
            writer.writerow([date,p[0],p[1],c,a])

    date += timedelta(days=1)