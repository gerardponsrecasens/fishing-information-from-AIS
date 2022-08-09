import netCDF4 as nc4
import csv
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


############# COORDINATES OF THE WANTED POINTS #####################

coords = pd.read_csv(r'.\1a_coordinates.csv')
points_lat = coords['Latitud'].to_numpy()
points_lon =  coords['Longitud'].to_numpy()
points = []
for i,j in zip(points_lat,points_lon):
    points.append([i,j])

########################### CREATE CSV ##############################

output_file = r'.\sla.csv'
with open(output_file, 'a', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(['Day','Latitude','Longitude','SLA'])

############################# INDEX ###################################
# The inout grid has a spacing of 0.5 and covers the whole globe (90 to -90, -180 to 180)

grid = 0.5
index_cop = []
for point in points:
    latitude = point[0]
    longitude = point[1]
    ilat = int(abs((90-latitude)/grid))
    ilon = int(abs((-180-longitude)/grid))
    index_cop.append([ilat,ilon])

######################## DATA ##########################################

path_sla = r'path_to_sla_file'
df = nc4.Dataset(path_sla)


############################ PREPROCESS ############################

n = len(df['z'])
sla = df['variable']

date = datetime(2017,1,1) #Date of the first file

for i in range(n):
    day = sla[i]
    with open(output_file, 'a', newline="", encoding='UTF8') as f:
        writer = csv.writer(f)
        for idx,p in zip(index_cop,points):
            writer.writerow([date,p[0],p[1],day[idx[0],idx[1]]])
    date += timedelta(days=1)