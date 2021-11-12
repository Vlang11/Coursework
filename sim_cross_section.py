#!/usr/bin/env python
# coding: utf-8

# <h2>Time-Height Area-Averaged Cross-Sections</h2>
# 
# This example demonstrates how to take 3-D WRF-ARW output from multiple times (in this case, using data from separate files), compute the area average of a field over a specified lat/lon range at each time, and create a time-height cross-section from the resulting data.
# 
# The example below plots the area-averaged temperature difference, potential temperature tendency, and water vapor mixing ratio (between 1000-100 hPa) over a small domain centered off of Florida peninsula from nine times (every 3 hr from 0000 UTC 25 August 2021 to 1200 UTC 26 August 2021), using data obtained from a WRF simulation with cu parameterization perturbed. 
# 
# More information on how to use wrf-python is available at https://wrf-python.readthedocs.io/en/main/basic_usage.html.
# 
# <hr>

# We start by importing the needed modules. These are drawn from four packages - netCDF4, matplotlib, numpy, and wrf (short for wrf-python). We do not need to load cartopy because there is no mapping involved. Note that wrf-python treats data as xarrays, which makes xarray functions (such as the sel function we use to subset data) available to us without loading xarray ourselv

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.ticker import (NullFormatter, ScalarFormatter)
import matplotlib.dates as mdates
from netCDF4 import Dataset
from wrf import to_np, getvar, ll_to_xy, ALL_TIMES


# Open all of the desired wrfout files and store the resulting Dataset entities to a variable

# Create Lists 
filelist1 = [Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-25_00:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-25_03:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-25_06:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-25_09:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-25_12:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-25_15:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-25_18:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-25_21:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-26_00:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-26_03:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-26_06:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-26_09:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/control/wrfout_d01_2021-08-26_12:00:00")]               
      
filelist2 = [Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-25_00:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-25_03:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-25_06:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-25_09:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-25_12:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-25_15:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-25_18:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-25_21:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-26_00:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-26_03:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-26_06:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-26_09:00:00"),
               Dataset("/home/valang/Working/WRF_Assignment4/WRF/test/em_real/perturbed/wrfout_d01_2021-08-26_12:00:00")]               

               


# The timeidx=ALL_TIMES option indicates to wrf-python to get data for all of the times included in the filelist variable. It relies on the ALL_TIMES import in the first code block above. The method="cat" option indicates to wrf-python to concatenate the data together - here, along the time axis given that the different wrfout files vary only in the time dimension.


#Extract pressure, temp and water vapor mixing ratio using ALL_TIMES and cat method
p1 = getvar(filelist1, "pressure", timeidx=ALL_TIMES, method="cat")
p2 = getvar(filelist2, "pressure", timeidx=ALL_TIMES, method="cat")
t1 = getvar(filelist1, "tc", timeidx=ALL_TIMES, method="cat") #temp in celcius
t2 = getvar(filelist2, "tc", timeidx=ALL_TIMES, method="cat")
qv1 = getvar(filelist1, "RQVCUTEN", timeidx=ALL_TIMES, method="cat") #water vapor mixing ratio
qv2 = getvar(filelist2, "RQVCUTEN", timeidx=ALL_TIMES, method="cat")
tt1 = getvar(filelist1, "RTHCUTEN", timeidx=ALL_TIMES, method="cat") #potential temp tendenency 
tt2 = getvar(filelist2, "RTHCUTEN", timeidx=ALL_TIMES, method="cat")

# Specify the latitude and longitude ranges over which to compute the area average, then use the wrf-python ll_to_xy helper function to convert these to x/y points. We call this helper function because the model variables have dimensions south_north and west_east, which refer to x/y points rather than to lat/lon location, and these variables are what we will later use to subset the data for the area average.
# 
# The pair lat1,lon1 refers to the southwestern corner of the domain, whereas the pair lat2,lon2 refers to the northeastern corner of the domain. The resulting x/y values provide us with the bounds for the area average to come.

# In[ ]:


lat1 = 32.0
lat2 = 36.0
lon1 = -93.0
lon2 = -87.0

x1, y1 = to_np(ll_to_xy(filelist1, lat1, lon1))
x2, y2 = to_np(ll_to_xy(filelist1, lat2, lon2))


# Subset the data from the full domain to just that associated with our area average. We use the xarray helper function sel() to do so. Note how we save the subset data to a new variable; this allows us to continue to work with the full dataset without reloading it if we wish to do so. We pass the subsetting bounds to each dimension (south_north and west_east) as slices, which are sequences of numbers from the first entry to the second entry.

# In[ ]:


p1_sub = p1.sel(south_north=slice(y1,y2), west_east=slice(x1,x2))
p2_sub = p2.sel(south_north=slice(y1,y2), west_east=slice(x1,x2))
t1_sub = t1.sel(south_north=slice(y1,y2), west_east=slice(x1,x2))
t2_sub = t2.sel(south_north=slice(y1,y2), west_east=slice(x1,x2))
tt1_sub = tt1.sel(south_north=slice(y1,y2), west_east=slice(x1,x2))
tt2_sub = tt2.sel(south_north=slice(y1,y2), west_east=slice(x1,x2))
qv1_sub = qv1.sel(south_north=slice(y1,y2), west_east=slice(x1,x2))
qv2_sub = qv2.sel(south_north=slice(y1,y2), west_east=slice(x1,x2))

# Find the difference between simulations for each variable 
# Assume pressure levels remain relatively the same between simulation runs to use as a surface
# at which other variables can be measured
t= t2_sub - t1_sub
tt= tt2_sub - tt1_sub
qv= qv2_sub - qv1_sub


# The area-average for each variable can be obtained using xarray's mean attribute function. For the microphysical parameterization heating rate, we only want the area average to be along the south_north and west_east dimensions. For pressure, however, we want the area-average to be along the south_north, west_east, and bottom_top dimensions. The latter relies on the assumption that the model's vertical surfaces are at nearly constant altitudes with time. This allows us to pass in a 1-D array of pressure levels for the y-axis when we plot the data. Caveat emptor!
# 
# The resulting hdiab_mean variable has two varying dimensions: Time (representing the time axis) and bottom_top (representing the model's vertical dimension). The latter has no values ascribed to it, however. The resulting p_mean variable has a single varying dimension: bottom_top.

# In[1]:


#hdiab_mean = hdiab_sub.mean(dim=['south_north', 'west_east'])
p_mean = p1_sub.mean(dim=['Time','south_north', 'west_east'])
t_mean = t.mean(dim=['south_north', 'west_east'])
tt_mean = tt.mean(dim=['south_north', 'west_east'])
qv_mean = qv.mean(dim=['south_north', 'west_east'])


# The remainder of the plot-generation code is contained in a single code block below. This is due to a Python quirk; a figure is generated before we add any data to it if we try to break the code up into separate code blocks. Please see the comment blocks below to interpret the code.


# Create the figure instance (9" wide by 6" tall,
# 200 dots per inch), then establish the figure's axes.
fig = plt.figure(figsize=(9,6), dpi=200.)
ax = plt.axes()

# Plot temp difference contours as a shaded field (which have a unique date/time structure) as
# the x-axis values and the time-averaged pressure variable
# as the y-axis values.Note that we have to transpose the
# display variable so that time corresponds to the x-axis
# rather than the y-axis (which is what matplotlib thinks
# it corresponds to given how the data are arranged in the
# array), and likewise for the vertical dimension.
t_contours = plt.contourf(t_mean.Time.values, p_mean,
                             t_mean.transpose(),
                             levels=np.arange(-3.,3.3,0.3),
                             cmap=get_cmap("viridis"), extend ='both')
plt.colorbar(t_contours, ax=ax, pad=.05, label="Temperature Difference")

# This set of code structures our x-axis. We first set
# the tick label size to 8pt font. We then set the
# date/time format of the tick labels to Day-Month-Year
# Hour:00. Finally, we rotate the tick labels to be
# mostly vertical rather than horizontal.
ax.tick_params(axis='x', labelsize=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b-%y %H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d-%b-%y %H:00"))
plt.xticks(rotation=60)

# This set of code structures our y-axis ticks and their labels.
# We first set the y-axis to be logarithmic rather than linear.
# Next, we set how the logarithmic axis labels should be structured,
# using scalars rather than powers of 10. Once we have
# done that, we define ten y-axis ticks from 100 to 1000 hPa.
# Finally, we set the y-axis limits - in this case, 1000-100 hPa,
# which ensures the y-axis decreases rather than increases upward.
ax.set_yscale('symlog')
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.set_yticks(np.linspace(100, 1000, 10))
ax.set_ylim(1000., 100.)

# Set the x-axis and y-axis labels.
ax.set_xlabel("Time (UTC)", fontsize=8)
ax.set_ylabel("Pressure (hPa)", fontsize=12)
plt.tight_layout()
# Title the plot and then display it.
plt.title("Area-Averaged [(" + str(lat1) + ", " + str(lon1) + ") to (" + str(lat2) + ", " + str(lon2) + ")] Temperature Difference (degree C)", loc="left", fontsize=10)
plt.savefig('areaavg_temp_cross_section')


fig = plt.figure(figsize=(9,6), dpi=200.)
ax = plt.axes()

tt_contours = plt.contourf(tt_mean.Time.values, p_mean, 
                             tt_mean.transpose()*86400.,
                             levels=np.arange(-6.0,6.5,0.5),
                             cmap=get_cmap("viridis"), extend ='both')
plt.colorbar(tt_contours, ax=ax, pad=.05, label="Potential Temperature Difference(K/day)")

ax.tick_params(axis='x', labelsize=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b-%y %H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d-%b-%y %H:00"))
plt.xticks(rotation=60)

ax.set_yscale('symlog')
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.set_yticks(np.linspace(100, 1000, 10))
ax.set_ylim(1000., 100.)

# Set the x-axis and y-axis labels.
ax.set_xlabel("Time (UTC)", fontsize=8)
ax.set_ylabel("Pressure (hPa)", fontsize=12)
plt.tight_layout()
# Title the plot and then display it.
plt.title("Area-Averaged [(" + str(lat1) + ", " + str(lon1) + ") to (" + str(lat2) + ", " + str(lon2) + ")] Potential Temperature Tendency Difference", loc="left", fontsize=10)
plt.savefig('potential_temp_cross_section')


fig = plt.figure(figsize=(9,6), dpi=200.)
ax = plt.axes()

qv_contours = plt.contourf(qv_mean.Time.values, p_mean, 
                             qv_mean.transpose()*86400000.,
                             levels=np.arange(-10,10.5,0.5),
                             cmap=get_cmap("viridis"), extend ='both')
plt.colorbar(qv_contours, ax=ax, pad=.05, label="Water Vapor Mixing Ratio Difference (g/kg*day)")

ax.tick_params(axis='x', labelsize=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b-%y %H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d-%b-%y %H:00"))
plt.xticks(rotation=60)

ax.set_yscale('symlog')
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.set_yticks(np.linspace(100, 1000, 10))
ax.set_ylim(1000., 100.)

# Set the x-axis and y-axis labels.
ax.set_xlabel("Time (UTC)", fontsize=8)
ax.set_ylabel("Pressure (hPa)", fontsize=12)
plt.tight_layout()
# Title the plot and then display it.
plt.title("Area-Averaged [(" + str(lat1) + ", " + str(lon1) + ") to (" + str(lat2) + ", " + str(lon2) + ")] Water Vaporing Mixing Ratio Tendency Difference", loc="left", fontsize=10)
plt.savefig('q_mixingratio_cross_section')

