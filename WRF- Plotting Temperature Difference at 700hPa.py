#!/usr/bin/env python
# coding: utf-8

# <h2>Plotting Simulation Differences</h2>
# 
# This example demonstrates how to use wrf-python to plot the differences between two output over multiple times.
# 
# More information on how to use wrf-python is available at https://wrf-python.readthedocs.io/en/main/basic_usage.html.
# 
# 
# We start by importing the needed modules. These are drawn from five packages - netCDF4, matplotlib, numpy, cartopy, and wrf (short for wrf-python).

# In[ ]:


from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import matplotlib.ticker as mticker
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, ll_to_xy, ALL_TIMES, interplevel)


# In[ ]:


# Create lists to loop through simulations
dates = ['25_06', '25_12', '25_18', '26_00', '26_06', '26_12']
dates2 = ['25_06', '25_12', '25_18', '26_00', '26_06', '26_12']
         
def addzero(value):
   if value < 10:
          return ("0" + str(value))
   else:
       return str(value)
   
# Loop through the dates/simulations
for date in dates:
   for date2 in dates2:
       # Open the datasets
       ncfile = Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-"+ date + ":00:00")
       ncfile2 = Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control//perturbed/wrfout_d01_2021-08-" + date2 + ":00:00")
   
   cont_temp = getvar(ncfile1, "tc") #Get temperature data from both cont and pert wrf file
   pert_temp = getvar(ncfile2, "tc")
   cont_pres = getvar(ncfile1, "pressure")  
   pert_pres = getvar(ncfile2, "pressure")
   cont_t = interplevel(cont_temp, cont_pres, 700)  #identify temperature at 700hPa level
   pert_t = interplevel(pert_temp, pert_pres, 700)

   lats, lons = latlon_coords(cont_pres)
   cart_proj = get_cartopy(cont_pres)

   # Create a figure instanc and set up map projection, boundaries etc.
   fig = plt.figure(figsize=(12,9), dpi=200.)
   ax = plt.axes(projection=cart_proj) 
   #add coastlines to the plot (resolution, linewidth)
   ax.coastlines('50m', linewidth = .8)
        
   #add the states
   ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor = 'grey', linewidth = 0.6)
      
   # Set the map bounds
   ax.set_xlim(cartopy_xlim(cont_t))
   ax.set_ylim(cartopy_ylim(cont_t))

   #Find difference in temperature between pert and cont simulation and plot contours every .25 degrees from -5 to 5C
   temp_diff = pert_t - cont_t
   plt.contourf(to_np(lons), to_np(lats), to_np(temp_diff), np.arange(-5.,5,0.25),
            transform=crs.PlateCarree(),cmap=get_cmap("PRGn"))

   plt.colorbar(ax=ax, shrink=.98)

   ax.set_extent([-90.,-60.,45.,15.],crs=crs.PlateCarree())

   gridlines = ax.gridlines(color="grey", linestyle="dotted", draw_labels=True)
   gridlines.xlabels_top = False
   gridlines.ylabels_right = False
   gridlines.xlocator = mticker.FixedLocator(np.arange(-90.,-60.,5.))
   gridlines.ylocator = mticker.FixedLocator(np.arange(15.,45.,5.))
   gridlines.xlabel_style = {'size':12, 'color':'black'}
   gridlines.ylabel_style = {'size':12, 'color':'black'}
   gridlines.xformatter = LONGITUDE_FORMATTER
   gridlines.yformatter = LATITUDE_FORMATTER
       
   plt.title("Shaded: 08/25/2021 0000 UTC Control minus 08/25/2021 0000 UTC Pertubation Temperature at 700hPa", loc="left")
   plt.savefig('T_Diff_700mb_' + '2021-08' + date + ':00:00' + '.png')


# In[ ]:





# In[ ]:




