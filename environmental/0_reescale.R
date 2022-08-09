# EXAMPLE OF REESCALE .NC FILES TO 0.5ºX0.5º GRID, FROM BOTH A BRICK FILE (ONE FILE
# WITH ALL DAYS) OR SIMPLE FILES (ONE DAY PER DAY).

# Import libraries
library(raster)
library(ncdf4)

# Import a reference .nc file, which is already scaled at 0.5ºx0.5º
r1 = raster('path_to_reference_.nc_file')

##### BRICK FILE #####

r2 = brick('src_path',varname='variable_name')
r3 = resample(r2,r1)
writeRaster(r3, 'dst_path')


##### NORMAL FILES #####

path = 'folder_path'

file_list <- list.files(path=path)


for (value in file_list) {
  p = paste(path,'/',value,sep='')
  r2 = raster(p,varname='variable_name')
  names(r2) = 'variable_name'
  r3 = resample(r2,r1)
  writeRaster(r3, paste('dst_folder',value,sep=''))
}