#!/usr/bin/env python
# coding: utf-8


from netCDF4 import Dataset

#file_name = "met_em.d01.2021-07-13_12:00:00.nc"
#directory_path = "/home/valang/WRF_Project/WRF/test/em_real/"
#open the netcdf file (location and file name, what to do with the file)
#r = read, a = append, w = write
#met_file = Dataset(file_name + directory_path, 'a')

dates = ['14_00','14_06','14_09','14_12','14_15','14_18', '14_21','15_00', '15_03', '15_06']

for date in dates:
    met_file = Dataset("/home/valang/Working/WRF_Project/WRF/test/em_real/met_em.d01.2021-07-"+ date + ":00:00.nc")

    '''
    Land Use Categories
    1 = Evergreen Needleleaf Forest
    2 = Evergreen Broadleaf Forest
    3 = Deciduous Needleleaf Forest
    4 = Deciduous Broadleaf Forest
    5 = Mixed Forests
    6 = Closed Shrublands
    7 = Open Shrublands
    8 = Woody Savannas
    9 = Savannas
    10 = Grasslands
    11 = Permanent Wetlands
    12 = Croplands
    13 = Urban and Built-Up
    14 = Cropland/Natural Vegetation Mosaic
    15 = Snow and Ice
    16 = Barren or Sparsely Vegetated
    17 = Water
    18 = Wooded Tundra
    19 = Mixed Tundra
    20 = Varren Tundra
    '''

    #open the netcdf variable object.  This is the object not the data.  We need this
    #so we can save the new data later
    landuse = met_file.variables['LU_INDEX']
    greenfrac = met_file.variables['GREENFRAC']

    #this extracts the data from the variable object.
    #[0,:] is used rather than [:] becasue netCDF always has a sigleton dimension when you extract the data
    landuse_data = landuse[0,:]

    #green frac -loop through 12 months
    greenfrac_data = greenfrac[0,:]
    greenfrac_data[:] = 100

    #if the land use is equal to crop land, change it to barren
    #landuse_data[landuse_data == 14] = 16
    landuse_data[:] = 14

    #set the data contained in the varible object to the new data we have created
    landuse[0,:] = landuse_data
    greenfrac[0,:] = greenfrac_data

    #close the netcdf file.  Changes are not saved until this command
    met_file.close()

