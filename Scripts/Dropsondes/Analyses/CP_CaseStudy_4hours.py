#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:45:05 2020

@author: annaleaalbright
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 17:44:46 2020

@author: annaleaalbright
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 17:13:35 2020

@author: annaleaalbright
"""

# =============================================================================
                # Import packages
# =============================================================================  
import numpy as np
from os.path import expanduser
import matplotlib.pyplot as plt
home = expanduser("~") # Get users home directory
plt.rcParams.update({'font.size': 28})
import xarray as xr
import glob

# Before
# 11:45 dropsonde 21, outside cold pool
# 11:55 dropsonde 23, inside cold pool
# 12:00 dropsonde 24, edge of cold pool (outside cold pool, inside cloud)

# =============================================================================
                #  Evolution in time
# =============================================================================  

########      Load data      ######
path1 = '/Users/annaleaalbright/Desktop/EUREC4A/Dropsondes/Processed_sondes_24012020/D20200124_115501_PQC.nc'
ori_list1 = xr.open_dataset(path1).dropna(dim='time',subset=['time']).\
swap_dims({'time':'alt'}).reset_coords().dropna(dim='alt',subset=['alt','pres','u_wind','v_wind','lat','lon','mr'],
         how='any').\
interp(alt=np.arange(0,9100,10))

path2= '/Users/annaleaalbright/Desktop/EUREC4A/Dropsondes/Processed_sondes_24012020/D20200124_125501_PQC.nc'
ori_list2 = xr.open_dataset(path2).dropna(dim='time',subset=['time']).\
swap_dims({'time':'alt'}).reset_coords().dropna(dim='alt',subset=['alt','pres','u_wind','v_wind','lat','lon','mr'],
         how='any').\
interp(alt=np.arange(0,9100,10))

path3= '/Users/annaleaalbright/Desktop/EUREC4A/Dropsondes/Processed_sondes_24012020/D20200124_135507_PQC.nc'
ori_list3 = xr.open_dataset(path3).dropna(dim='time',subset=['time']).\
swap_dims({'time':'alt'}).reset_coords().dropna(dim='alt',subset=['alt','pres','u_wind','v_wind','lat','lon','mr'],
         how='any').\
interp(alt=np.arange(0,9100,10))

path4= '/Users/annaleaalbright/Desktop/EUREC4A/Dropsondes/Processed_sondes_24012020/D20200124_145504_PQC.nc'
ori_list4 = xr.open_dataset(path4).dropna(dim='time',subset=['time']).\
swap_dims({'time':'alt'}).reset_coords().dropna(dim='alt',subset=['alt','pres','u_wind','v_wind','lat','lon','mr'],
         how='any').\
interp(alt=np.arange(0,9100,10))

path5= '/Users/annaleaalbright/Desktop/EUREC4A/Dropsondes/Processed_sondes_24012020/D20200124_155507_PQC.nc'
ori_list5 = xr.open_dataset(path5).dropna(dim='time',subset=['time']).\
swap_dims({'time':'alt'}).reset_coords().dropna(dim='alt',subset=['alt','pres','u_wind','v_wind','lat','lon','mr'],
         how='any').\
interp(alt=np.arange(0,9100,10))

# OUTSIDE cold pool 11:45 am
path_outside = '/Users/annaleaalbright/Desktop/EUREC4A/Dropsondes/Processed_sondes_24012020/D20200124_114503_PQC.nc'
ori_list6 = xr.open_dataset(path_outside).dropna(dim='time',subset=['time']).\
swap_dims({'time':'alt'}).reset_coords().dropna(dim='alt',subset=['alt','pres','u_wind','v_wind','lat','lon','mr'],
         how='any').\
interp(alt=np.arange(0,9100,10))


#%%
maxheight = 1000 # choose maximum height to cut off plot

# subplot of zonal + meridional wind; theta_e, theta_v, mixing ratio, relative humiditiy
fig, ax = plt.subplots(2,3,figsize=(30,30))
ax[0,0].plot(ori_list1['u_wind'], ori_list1['alt'], linewidth=4, label='11:55')
ax[0,0].plot(ori_list2['u_wind'], ori_list2['alt'], linewidth=4, label='12:55')
ax[0,0].plot(ori_list3['u_wind'], ori_list3['alt'], linewidth=4, label='13:55')
ax[0,0].plot(ori_list4['u_wind'], ori_list4['alt'], linewidth=4, label='14:55')
ax[0,0].plot(ori_list5['u_wind'], ori_list5['alt'], linewidth=4, label='15:55')
ax[0,0].plot(ori_list6['u_wind'], ori_list6['alt'], linewidth=6, color="k", label="outside cold pool")
ax[0,0].set_xlabel('zonal wind speed (m/s)')
ax[0,0].set_xlim([-10,0])
ax[0,0].set_ylabel('altitude (m)')
ax[0,0].set_ylim(np.min(ori_list1['alt']), maxheight)
ax[0,0].spines['right'].set_visible(False)
ax[0,0].spines['top'].set_visible(False)
#ax[0,0].legend(loc='best')

ax[0,1].plot(ori_list1['v_wind'], ori_list1['alt'], linewidth=4)
ax[0,1].plot(ori_list2['v_wind'], ori_list2['alt'], linewidth=4)
ax[0,1].plot(ori_list3['v_wind'], ori_list3['alt'], linewidth=4)
ax[0,1].plot(ori_list4['v_wind'], ori_list4['alt'], linewidth=4)
ax[0,1].plot(ori_list5['v_wind'], ori_list5['alt'], linewidth=4)
ax[0,1].plot(ori_list6['v_wind'], ori_list6['alt'], linewidth=6, color="k")
ax[0,1].set_xlabel('meridional wind speed (m/s)')
ax[0,1].set_xlim([-3,8])
ax[0,1].set_ylim(np.min(ori_list1['alt']), maxheight)
ax[0,1].spines['right'].set_visible(False)
ax[0,1].spines['top'].set_visible(False)

ax[0,2].plot(ori_list1['theta_e'], ori_list1['alt'], linewidth=4)
ax[0,2].plot(ori_list2['theta_e'], ori_list2['alt'], linewidth=4)
ax[0,2].plot(ori_list3['theta_e'], ori_list3['alt'], linewidth=4)
ax[0,2].plot(ori_list4['theta_e'], ori_list4['alt'], linewidth=4)
ax[0,2].plot(ori_list5['theta_e'], ori_list5['alt'], linewidth=4)
ax[0,2].plot(ori_list6['theta_e'], ori_list6['alt'], linewidth=6,color="k")
ax[0,2].set_xlabel('equivalent potential temp (K)')
ax[0,2].set_ylim(np.min(ori_list1['alt']), maxheight)
ax[0,2].spines['right'].set_visible(False)
ax[0,2].spines['top'].set_visible(False)
ax[0,2].set_xlim([330,347])

ax[1,0].plot(ori_list1['theta_v'], ori_list1['alt'], linewidth=4)
ax[1,0].plot(ori_list2['theta_v'], ori_list2['alt'], linewidth=4)
ax[1,0].plot(ori_list3['theta_v'], ori_list3['alt'], linewidth=4)
ax[1,0].plot(ori_list4['theta_v'], ori_list4['alt'], linewidth=4)
ax[1,0].plot(ori_list5['theta_v'], ori_list5['alt'], linewidth=4)
ax[1,0].plot(ori_list6['theta_v'], ori_list6['alt'], linewidth=6,color="k")
ax[1,0].set_xlabel('virtual potential temp (K)')
ax[1,0].set_ylabel('altitude (m)')
ax[1,0].set_ylim(np.min(ori_list1['alt']), maxheight)
ax[1,0].spines['right'].set_visible(False)
ax[1,0].spines['top'].set_visible(False)
ax[1,0].set_xlim([299,305])

ax[1,1].plot(ori_list1['mr'], ori_list1['alt'], linewidth=4)
ax[1,1].plot(ori_list2['mr'], ori_list2['alt'], linewidth=4)
ax[1,1].plot(ori_list3['mr'], ori_list3['alt'], linewidth=4)
ax[1,1].plot(ori_list4['mr'], ori_list4['alt'], linewidth=4)
ax[1,1].plot(ori_list5['mr'], ori_list5['alt'], linewidth=4)
ax[1,1].plot(ori_list6['mr'], ori_list6['alt'], linewidth=6,color="k")
ax[1,1].set_xlabel('mixing ratio (g/kg)')
ax[1,1].set_ylim(np.min(ori_list1['alt']), maxheight)
plt.sca(ax[1,1])
ax[1,1].spines['right'].set_visible(False)
ax[1,1].spines['top'].set_visible(False)
ax[1,1].set_xlim([10,18])


ax[1,2].plot(ori_list1['rh'], ori_list1['alt'], linewidth=4)
ax[1,2].plot(ori_list2['rh'], ori_list2['alt'], linewidth=4, label='before cold pool (11:45am)')
ax[1,2].plot(ori_list3['rh'], ori_list3['alt'], linewidth=4, label='after cold pool (12:00pm)')
ax[1,2].plot(ori_list4['rh'], ori_list4['alt'], linewidth=4, label='after cold pool (12:00pm)')
ax[1,2].plot(ori_list5['rh'], ori_list5['alt'], linewidth=4, label='after cold pool (12:00pm)')
ax[1,2].plot(ori_list6['rh'], ori_list6['alt'], linewidth=6, color="k", label='after cold pool (12:00pm)')
ax[1,2].set_xlabel('relative humidity (%)')
ax[1,2].set_ylim(np.min(ori_list1['alt']), maxheight)
ax[1,2].spines['right'].set_visible(False)
ax[1,2].spines['top'].set_visible(False)
ax[1,2].set_xlim([50, 100])


#ax[0,0].plot(combined['u_wind'].mean(dim='sonde_no').values, combined['alt'], color="k",linewidth=6)
#ax[0,1].plot(combined['v_wind'].mean(dim='sonde_no').values, combined['alt'], color="k",linewidth=6)
#ax[0,2].plot(combined['theta_e'].mean(dim='sonde_no').values, combined['alt'],color="k", linewidth=6)
#ax[1,0].plot(combined['theta_v'].mean(dim='sonde_no').values, combined['alt'],color="k", linewidth=6)
#ax[1,1].plot(combined['mr'].mean(dim='sonde_no').values, combined['alt'],color="k", linewidth=6)
#ax[1,2].plot(combined['rh'].mean(dim='sonde_no').values, combined['alt'],color="k", linewidth=6)

# u, v, thetav, theta_e, mr, rh 
#%% Extra code from Geet

directory = '/Users/annaleaalbright/Desktop/EUREC4A/Dropsondes/Processed_sondes_24012020/'

allfiles = sorted(glob.glob(directory + 'D*_PQC.nc'))

# sorting all files in the directory

ori_list = [None] * len(allfiles)

g = 0 # counter

for i in allfiles :
    ori_list[g] = xr.open_dataset(i).dropna(dim='time',subset=['time']).\
                      swap_dims({'time':'alt'}).reset_coords().dropna(dim='alt',subset=['alt','pres','u_wind','v_wind','lat','lon','mr'],
                         how='any').\
                  interp(alt=np.arange(0,9100,10))
    g = g + 1

combined = xr.concat(ori_list[:], dim="sonde_no")

