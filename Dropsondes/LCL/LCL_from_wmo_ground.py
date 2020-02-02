#!/usr/bin/env python
# coding: utf-8

# In[77]:


#!/usr/bin/env python
import sys
from optparse import OptionParser
import numpy as np
import matplotlib.pyplot as plt
import glob
import metpy
import metpy.calc as mpcalc
from metpy.units import units
import sys; sys.argv=['']; #del sys
import xarray as xr
from datetime import datetime

import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as mdates

##### decoding functions ##########
def dectemp(daten):
#  decode temperature and dewpoint
    if (daten[0:3]!='///'):
        temp = (float(daten[0:3])*0.1); tsign = int(daten[2:3])
        if (tsign%2 == 1): temp = -1 * temp
        if (daten[3:5]!='//'):
            dewd = int(daten[3:5])
            dewdp = dewd*0.1 if (dewd<55) else dewd-50 
            dewp = temp - dewdp 
        else:
            dewp = np.nan
    else:
        temp = np.nan; dewp = np.nan
    return(temp,dewp)
###

def decwind(daten,windkt):
#  decode wind direction and speed
    if (daten[0:2]!='//') and (daten[2:5]!='///'):
        wdir = float(daten[0:2])*10.0
        wspd = float(daten[2:5])
        if (wspd > 500): 
            wspd -= 500; wdir += 5
        if (not windkt):
            wspd *= 1.943844
    else:
        wdir = np.nan; wspd = np.nan
    return(wdir,wspd)
###
def dechght(daten,prest):
# decode height in AA section
    height = float(daten)
    if (prest==850.0): height += 1000.0
    if (prest==700.0): 
            height = height+2000.0 if (height>500) else height+3000.0
    if (prest<=500.0): height *= 10.0
    if (prest<=250.0) and (height<7500): height += 10000
    return(height)


# In[59]:


allfiles = sorted(glob.glob('*.wmo'))
# sorting all files in the directory 

lcl_p = [None] * len(allfiles)
lcl_t = [None] * len(allfiles)
time_id = [None] * len(allfiles)
lat = [None] * len(allfiles)
lon = [None] * len(allfiles)

for id_k,k in enumerate(allfiles) :

    args = []

    # usage = "usage: %test_drops.py D20200124_100525.wmo (WMO levels)"
    # parser = OptionParser(usage=usage)
    # (options, args) = parser.parse_args()

    args.append(k)

    if len(args) == 0:
        print("ERROR: no dropsonde file selected")
        sys.exit(1)

    #  date is not encoded in FM37
    jah = '2020'
    mon = '01'
    #  check for date in filename
    if (args[0].find('D202')>=0):
        jah = args[0][args[0].find('D202')+1:][:4]
        mon = args[0][args[0].find('D202')+5:][:2]
    sond_data = open(args[0],'rU').readlines()


    for line in sond_data:
        lines = line.strip()
        if (lines.find('HEAD')>=0) or (sond_data.index(line)==0): 
            tag = lines[-6:-4]
        if (lines.find('XXAA')>=0):
            aa_start = sond_data.index(line)
        if (lines.find('XXBB')>=0):
            bb_start = sond_data.index(line)
        if (lines.find('62626')>=0):
            l62 = lines
            if (lines.find('=')<0):
                l62 += sond_data[sond_data.index(line)+1].strip()                    
            rstd = l62[l62.find('REL')+16:][:2]
            rmin = l62[l62.find('REL')+18:][:2]
            rsec = l62[l62.find('REL')+20:][:2]
            rlat = float(l62[l62.find('REL')+4:][:4])*0.01
            rqla = l62[l62.find('REL')+8:][:1]
            rlon = float(l62[l62.find('REL')+9:][:5])*0.01
            rqlo = l62[l62.find('REL')+14:][:1]
            if (l62.find('SPG')>=0):
                sstd = l62[l62.find('SPG')+16:][:2]
                smin = l62[l62.find('SPG')+18:][:2]
                ssec = l62[l62.find('SPG')+20:][:2]
                slat = float(l62[l62.find('SPG')+4:][:4])*0.01
                sqla = l62[l62.find('SPG')+8:][:1]
                slon = float(l62[l62.find('SPG')+9:][:5])*0.01
                sqlo = l62[l62.find('SPG')+14:][:1]
            if (l62.find('SPL')>=0):
                sstd = l62[l62.find('SPL')+16:][:2]
                smin = l62[l62.find('SPL')+18:][:2]
                ssec = '00' # l62[l62.find('SPL')+20:][:2]
                slat = float(l62[l62.find('SPL')+4:][:4])*0.01
                sqla = l62[l62.find('SPL')+8:][:1]
                slon = float(l62[l62.find('SPL')+9:][:5])*0.01
                sqlo = l62[l62.find('SPL')+14:][:1]

#     print('Dropsonde: %s-%s-%s'% (jah, mon, tag))
#     print('released:  %.2f%s %.2f%s at %s:%s:%s'%(rlat,rqla,rlon,rqlo,rstd,rmin,rsec))
#     if (l62.find('SPG')>=0) or (l62.find('SPL')>=0):
#         print('splashed:  %.2f%s %.2f%s at %s:%s:%s'%(slat,sqla,slon,sqlo,sstd,smin,ssec))

    prest=[]; hght=[]; temp=[]; dewp=[]; presw = []; wdir = []; wspd = []

    #  join sections AA, BB
    textaa = sond_data[aa_start].strip()
    for i in range(aa_start+1,bb_start):
        line = sond_data[i].strip() 
        textaa += ' ' + line if (sond_data[i-1][0:5]!='62626') else line
        if (line.find('=')>0): break

    textbb = sond_data[bb_start].strip()
    for i in range(bb_start+1,len(sond_data)):
        line = sond_data[i].strip()
        textbb += ' ' + line if (sond_data[i-1][0:5]!='62626') else line
        if (line.find('=')>0): break

            #  XXAA section    
    daten = textaa[:-1].split(None)  
    day = int(daten[1][0:2]); hrs = daten[1][2:4]
    mwl = daten[1][4:5]; mwl = -9.9 if (mwl=='/') else float(mwl)*100.0
    if (mwl == 0.0): mwl = 1000.0
    #print 'Max wind level AA section:', mwl
    if(day>40):
        day = day - 50
        windkt = True
    else:
        windkt = False
    #  location
    if (daten[2][0:2]=='99'):
        rla = float(daten[2][2:5])*0.1; qla = daten[3][0:1]; ula = daten[4][3:4]
        rlo = float(daten[3][1:5])*0.1; qlo = daten[4][0:3]; ulo = daten[4][4:5]
    #  surface data
    if (daten[5][0:2]=='99'):
        prest.append(float(daten[5][2:5]))
        if (prest[-1]<100): prest[-1] += 1000.0
        hght.append(np.nan)
        (tp,dp) = dectemp(daten[6]); temp.append(tp); dewp.append(dp) 
        
    #  standard level data
    i = 8 # +9999
    while (i < len(daten)):
        prest.append(float(daten[i][0:2])*10)
        if (prest[-1]==0.0): prest[-1] = 1000.0
        if (prest[-1]==920.0): prest[-1] = 925.0
        if (prest[-1]==770.0) or (prest[-1]==660.0): 
            prest.pop()
                 
        if (prest[-1]==880.0):
            if (daten[i][2:5]!='999'):
                prest[-1] = float(daten[i][2:5])
            else:
                prest.pop()
                break
        if (daten[i][2:5]!='///') and (daten[i]!='88'):
            hg = dechght(daten[i][2:5],prest[-1]); hght.append(hg)
        else:
            hght.append(np.nan)
        (tp,dp) = dectemp(daten[i+1]); temp.append(tp); dewp.append(dp) 
        if (daten[i][0:2]=='88'): 
            print('  tropopause detected at', prest[-1], ':', temp[-1])
        i += 2
        presw.append(prest[-1])
        if (prest[-1]>=mwl) and (mwl > 0):

            (wd,ws) = decwind(daten[i],windkt); wdir.append(wd); wspd.append(ws)
            i += 1
        else:
            wdir.append(np.nan); wspd.append(np.nan)

    #  XXBB section signifcant levels
    daten = textbb[:-1].split(None)  
    i = 5 # +9999
    #  significant levels temperature
    while (i < len(daten)):
        if (daten[i]=='21212'):
    #        print '-----'
            i += 1
            break
        if (daten[i][2:5]!='///'):
            prest.append(float(daten[i][2:5]))
            if (prest[-1]<=100.0): prest[-1] += 1000.0
            hght.append(np.nan)
            (tp,dp) = dectemp(daten[i+1]); temp.append(tp); dewp.append(dp) 
        i += 2
    #    print prest[-1],hght[-1],temp[-1],dewp[-1]
    
    #  sort temperature levels
    prest,hght,temp,dewp = (list(t) for t in zip(*sorted(zip(prest,hght,temp,dewp))))  

    lcl_p[id_k], lcl_t[id_k] = (
        #     #lcl_p and lcl_t are the values of pressure and temperature at LCL, respectively

                            metpy.calc.lcl(prest[-3]*units.mbar,
                            # mean of pressure for all sondes from 0 to 210 m

                            temp[-3]*units.degC,
                            # mean of air temperature for all sondes from 0 to 210 m

                            dewp[-3]*units.degC,

                                          max_iters=200) )
                            # mean of dew point temperature for all sondes from 0 to 210 m
        
    time_id[id_k] = np.datetime64(datetime.strptime(jah + mon + tag + str(rstd)+str(rmin),
                                                    '%Y%m%d%H%M'))
    lat[id_k] = rlat
    lon[id_k] = rlon
    lcl_p[id_k] = np.float64(lcl_p[id_k].magnitude)
    lcl_t[id_k] = np.float64(lcl_t[id_k].magnitude)
    
    print('LCL Pressure for ' + str(rstd) + ':' + str(rmin) 
          + ' UTC is ' + str(round(lcl_p[id_k],2)) + ' hPa.')
    print('LCL Temperature for ' + str(rstd) + ':' + str(rmin) 
          + ' UTC is ' + str(round(lcl_t[id_k],2)) + ' ' + chr(176)+'C.')
    print('-------------')


# In[60]:


ds = xr.Dataset({'lcl_p'               : (['time'],lcl_p),
                 'lcl_t'            : (['time'],lcl_t),
                 'lat'            : (['time'],lat),
                 'lon'            : (['time'],lon),
                 },
                 coords={'time': time_id})

ds.to_netcdf('lcl.nc')


# In[79]:


sel_lon = 58 

plt.plot(ds['time'].where(ds['lon'] < sel_lon,drop=True).values,
         ds['lcl_p'].where(ds['lon'] < sel_lon,drop=True).values,
        marker='o')
myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)
plt.legend(frameon=False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.xlabel('Time / UTC')
plt.ylabel('Pressure / hPa')
plt.savefig('lcl_p_vs_time.png')

