# Import necessary packages
from netCDF4 import Dataset
from wrf import getvar, interplevel, vinterp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from metpy.plots.ctables import registry
mpl.use("Agg")
from matplotlib.cm import get_cmap
import matplotlib.ticker as mticker
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, ll_to_xy, ALL_TIMES, interplevel)

# Create lists to loop through simulations
dates = ['14_01','14_02','14_03','14_04','14_05','14_06','14_07','14_08','14_09','14_10','14_11','14_12','14_13','14_14','14_15', 
         '14_16', '14_17', '14_18', '14_19', '14_20', '14_21', '14_22', '14_23', '15_00', '15_01', '15_02', '15_03', '15_04', '15_05', '15_06']

def addzero(value):
   if value < 10:
          return ("0" + str(value))
   else:
       return str(value)
   
interval = np.arange(10,85,5)   
colormap = 'BuPu'
   
# Loop through the dates/simulations
for date in dates:
   ncfile1 = Dataset("/home/valang/Working/WRF_Project/WRF/test/em_real/wrf_control/wrfout_d01_2021-07-"+ date + ":00:00")
   ncfile2 = Dataset("/home/valang/Working/WRF_Project/WRF/test/em_real/wrf_perturbed/wrfout_d01_2021-07-" + date + ":00:00")
   
   cont_u = getvar(ncfile1, "ua") #  get u
   pert_u = getvar(ncfile2, "ua")
   cont_v = getvar(ncfile1, "va") #  get v
   pert_v = getvar(ncfile2, "va")
   
   cont_u10 = getvar(ncfile1, "U10") #  get u at surf
   pert_u10 = getvar(ncfile2, "U10")
   cont_v10 = getvar(ncfile1, "V10") #  get v at surf
   pert_v10 = getvar(ncfile2, "V10")
   
   cont_z = getvar(ncfile1, "z") #get heights
   pert_z = getvar(ncfile2, "z")
   cont_terh = getvar(ncfile1,"ter", meta=False) #get terrain height
   pert_terh = getvar(ncfile1,"ter", meta=False)
   cont_pres = getvar(ncfile1, "pressure")  #get pressure
   pert_pres = getvar(ncfile2, "pressure")
   
   cont_sixkm = cont_terh + 6000 #find 6km above terrain
   pert_sixkm = pert_terh + 6000
   
   cont_u6km = interplevel(cont_u, cont_z, cont_sixkm) #interpolate to 6km wind
   cont_v6km = interplevel(cont_v, cont_z, cont_sixkm)   
   pert_u6km= interplevel(pert_u, cont_z, pert_sixkm)
   pert_v6km = interplevel(pert_v, cont_z, pert_sixkm) 
   
   lats, lons = latlon_coords(cont_pres) #get lat/lons
   cart_proj = get_cartopy(cont_pres)  #get projection 
   
   cont_shearu = cont_u6km - cont_u10  #find shear components
   cont_shearv = cont_v6km - cont_v10
   pert_shearu = pert_u6km - pert_u10
   pert_shearv = pert_v6km - pert_v10 
   
   cont_shear = ((cont_shearu **2) + (cont_shearv **2))**0.5 #calc shear
   pert_shear = ((pert_shearu **2) + (pert_shearv **2))**0.5
   
   # Plot control simulation shear
   # Create a figure instanc and set up map projection, boundaries etc.
   fig = plt.figure(figsize=(12,9), dpi=200.) 
   ax = plt.axes(projection=cart_proj) 
   #add coastlines to the plot (resolution, linewidth)
   ax.coastlines('50m', linewidth = .8)
        
   #add the states
   ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor = 'grey', linewidth = 0.6)
      
   # Set the map bounds
   ax.set_xlim(cartopy_xlim(cont_pres))
   ax.set_ylim(cartopy_ylim(cont_pres))

   plt.contourf(to_np(lons), to_np(lats), to_np(cont_shear), np.arange(0.,62,2),
            transform=crs.PlateCarree(), cmap=colormap, extend = 'both')
   cb = plt.colorbar()
   cb.set_label("0-6km Wind Shear (m/s)")
   
   ax.set_extent([-98.,-89.,45.,39.],crs=crs.PlateCarree())

   gridlines = ax.gridlines(color="grey", linestyle="dotted", draw_labels=True)
   gridlines.xlabels_top = False
   gridlines.ylabels_right = False
   gridlines.xlocator = mticker.FixedLocator(np.arange(-98.,-89.,2.))
   gridlines.ylocator = mticker.FixedLocator(np.arange(39.,45.,2.))
   gridlines.xlabel_style = {'size':8, 'color':'black'}
   gridlines.ylabel_style = {'size':12, 'color':'black'}
   gridlines.xformatter = LONGITUDE_FORMATTER
   gridlines.yformatter = LATITUDE_FORMATTER
       
   plt.title("2021-07-" + date +":00:00 UTC Control Simulation 0-6km Shear", loc="left")
   plt.savefig('control_shear_2021-08-' + date + ':00:00' + '.png')
      
   # Plot Perturbation simulation shear
   # Create a figure instanc and set up map projection, boundaries etc.
   fig = plt.figure(figsize=(12,9), dpi=200.)
   ax = plt.axes(projection=cart_proj) 
   #add coastlines to the plot (resolution, linewidth)
   ax.coastlines('50m', linewidth = .8)
        
   #add the states
   ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor = 'grey', linewidth = 0.6)
      
   # Set the map bounds
   ax.set_xlim(cartopy_xlim(pert_pres))
   ax.set_ylim(cartopy_ylim(pert_pres))

   #Find difference in temperature between pert and cont simulation and plot contours every .25 degrees from -5 to 5C
   #temp_diff = pert_rad - cont_rad
   
   plt.contourf(to_np(lons), to_np(lats), to_np(pert_shear), np.arange(0.,62,2), 
            transform=crs.PlateCarree(), cmap=colormap, extend = 'both')
   cb = plt.colorbar()
   cb.set_label("0-6km Wind Shear (m/s)")

   ax.set_extent([-98.,-89.,45.,39.],crs=crs.PlateCarree())
   
   gridlines = ax.gridlines(color="grey", linestyle="dotted", draw_labels=True)
   gridlines.xlabels_top = False
   gridlines.ylabels_right = False
   gridlines.xlocator = mticker.FixedLocator(np.arange(-98.,-89.,2.))
   gridlines.ylocator = mticker.FixedLocator(np.arange(39.,45.,2.))
   gridlines.xlabel_style = {'size':8, 'color':'black'}
   gridlines.ylabel_style = {'size':12, 'color':'black'}
   gridlines.xformatter = LONGITUDE_FORMATTER
   gridlines.yformatter = LATITUDE_FORMATTER
       
   plt.title("2021-07-" + date +":00:00 UTC Pertubation Simulation 0-6km Shear", loc="left")
   plt.savefig('pert_shear_2021-08-' + date + ':00:00' + '.png')
   
  # Plot perturbation minus control simulation shear (difference)
   shear = pert_shear - cont_shear 
   # Create a figure instanc and set up map projection, boundaries etc.
   fig = plt.figure(figsize=(12,9), dpi=200.) 
   ax = plt.axes(projection=cart_proj) 
   #add coastlines to the plot (resolution, linewidth)
   ax.coastlines('50m', linewidth = .8)
        
   #add the states
   ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor = 'grey', linewidth = 0.6)
      
   # Set the map bounds
   ax.set_xlim(cartopy_xlim(cont_pres))
   ax.set_ylim(cartopy_ylim(cont_pres))

   plt.contourf(to_np(lons), to_np(lats), to_np(cont_shear), np.arange(-30.,40,2),
            transform=crs.PlateCarree(), cmap=colormap, extend = 'both')
   cb = plt.colorbar()
   cb.set_label("0-6km Wind Shear (m/s)")
   
   ax.set_extent([-98.,-89.,45.,39.],crs=crs.PlateCarree())

   gridlines = ax.gridlines(color="grey", linestyle="dotted", draw_labels=True)
   gridlines.xlabels_top = False
   gridlines.ylabels_right = False
   gridlines.xlocator = mticker.FixedLocator(np.arange(-98.,-89.,2.))
   gridlines.ylocator = mticker.FixedLocator(np.arange(39.,45.,2.))
   gridlines.xlabel_style = {'size':8, 'color':'black'}
   gridlines.ylabel_style = {'size':12, 'color':'black'}
   gridlines.xformatter = LONGITUDE_FORMATTER
   gridlines.yformatter = LATITUDE_FORMATTER
       
   plt.title("2021-07-" + date +":00:00 UTC Pertubation Minus Control Simulation 0-6km Shear", loc="left")
   plt.savefig('diff_shear_2021-08-' + date + ':00:00' + '.png')

   
