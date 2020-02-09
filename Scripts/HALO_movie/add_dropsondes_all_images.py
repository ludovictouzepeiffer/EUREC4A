# by Benjamin Fildier

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import xarray as xr
import os,sys,glob
import datetime

from PIL import Image,ImageSequence
from matplotlib.patches import Circle
import matplotlib.ticker as ticker
from matplotlib.colors import LinearSegmentedColormap


def imageNameRoot(dtime):

    """Takes the current datetime and rounds it to the nearest 10mn increment."""
    
    date_str = dtime.strftime('%Y-%m-%d')
        
    minutes = dtime.minute
    
    # pick time rounded to closest 10mn increment
    hr_goes = dtime.hour
    min_goes = round(dtime.minute/10)*10 # round min to closest 10mn
    hr_goes += int((min_goes/60)) # increment if round to next hour
    min_goes = min_goes%60
    dtime_goes = datetime.datetime(year=dtime.year,
                                   month=dtime.month,
                                   day=dtime.day,
                                   hour=hr_goes,
                                   minute=min_goes)
    
    # path of image
    nameroot = dtime_goes.strftime('%Y-%m-%dT%H:%M')
    
    return nameroot

def loadImage(dtime):
    
    """Load GOES image at closest 10mn increment
    Arguments:
    - dtime: datetime object
    """
    
    nameroot = imageNameRoot(dtime)
    
    # path of image
    fullpath = os.path.join(goesdir,nameroot[:10],nameroot+':00Z.jpg')
    print('load image %s:00Z.jpg'%nameroot)
    
    # load and return image
    return Image.open(fullpath)

def outputFileName(dtime):
    
    """Formats current date to name of output image file"""

    nameroot = dtime.strftime('%Y-%m-%dT%H:%M')
    
    return nameroot+'Z_HALO.jpeg' # and file extension
    
def loadSondes(dtime):
    
    """Load all sonde data as a list xarrays for current flight day"""

    allsondefiles = glob.glob(os.path.join(sondedir,
                                       dtime.strftime('%Y%m%d'),
                                       'AVAPS_Dropsondes/processed/*_PQC.nc'))
    allsondefiles.sort()
    
    allsondes = []
    
    for filepath in allsondefiles:
        
        allsondes.append(xr.open_dataset(filepath).dropna(dim='time',subset=['time']).swap_dims({'time':'alt'}).reset_coords().dropna(dim='alt',subset=['alt','time','lat','lon'],
                            how='any'))
    
    return allsondes

def getMatchingSondes(allsondes,dtime,dt_fade,verbose=False):
    
    """
    Find the sondes to be displayed on the image, including those currently recording
    and those fallen in the ocean but still appearing on the image.

    Arguments:
    - allsondes: list of all sondes already loaded
    - dtime: datetime object, current time
    - dt_fade: time window (mn) to fade out sondes that reached the surface
    
    Returns:
    - sondes: list of xarray objects"""
    
    sondes = []
    
    # window for fading out sonde display
    delta_fade = datetime.timedelta(minutes=dt_fade)
    
    for sonde in allsondes:
        
        launch_time = datetime.datetime.strptime(str(sonde.launch_time.values)[:16],
                                                '%Y-%m-%dT%H:%M')

        # If sonde currently falling or fell in the past dt_fade mn
        if launch_time <= dtime and launch_time + delta_fade > dtime:
                
            if verbose:
                print('keep ',launch_time)
                
            # Then load sonde data and store it
            sondes.append(sonde)
            
    return sondes

def showTime(ax,dtime):

    """Display current time on the upper left corner of GOES image"""
    
    ax.text(lonmin+0.1,latmax-0.45,dtime.strftime('%Y-%m-%d\n%H:%M UTC'),
            color='white',fontsize=30)

def showSonde(ax,dtime,sonde,cmap_falling=plt.cm.GnBu,altmax=9100,col_fading='darkorange',showtime=True):
    
    """Display sonde on GOES image. Colors are: green if being launched, calculated based on height using cmap_falling if still in the air, or col_fading (default 'darkorange') if at the surface"""

    dtime_str = dtime.strftime('%Y-%m-%dT%H:%M')
    sonde_times = np.array([str(sonde.time[i].values)[:16] for i in range(sonde.time.size)])
    matching_times = np.where(sonde_times == dtime_str)[0]

    if matching_times.size == 0: # no matching time, sonde on the ground
        falling = False
        i_dtime = 0
    else:
        falling = True
        i_dtime = matching_times[-1]
        
    # position of sonde at current time
    lon_sonde = sonde.lon.values[i_dtime]
    lat_sonde = sonde.lat.values[i_dtime]
    alt_sonde = sonde.alt.values[i_dtime]
    time_sonde = datetime.datetime.strptime(str(sonde.time.values[i_dtime])[:16],'%Y-%m-%dT%H:%M')
    launch_time = datetime.datetime.strptime(str(sonde.launch_time.values)[:16],'%Y-%m-%dT%H:%M')
    last_time = datetime.datetime.strptime(str(sonde.time.values[0])[:16],'%Y-%m-%dT%H:%M')
    
    # choose color based on height
    cNorm = colors.Normalize(vmin=0, vmax=altmax)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap_falling)
    fc = ec = scalarMap.to_rgba(alt_sonde)
    
    # color in darkorange if the sonde reached the ocean
    if dtime > last_time:
        fc = ec = col_fading
    # fix color for when sonde is just being launched
    if dtime == launch_time:
        fc = ec = col_top
    
    if falling:
        # color based on height
        alpha = 1
    else:
        # fade out coefficient
        delta_fade = datetime.timedelta(minutes=dt_fade)
        alpha = ((time_sonde+delta_fade)-dtime)/(delta_fade)
        if alpha > 1: alpha = 1 # correct for time rounding errors leading to alpha>1
        
    circ = Circle((lon_sonde,lat_sonde),0.03,linewidth=2,ec=ec,fc=fc,alpha=alpha)
    ax.add_patch(circ)
    
    # Show launch time
    if showtime:
        ax.text(lon_sonde+0.05,lat_sonde+0.05,str(sonde.launch_time.values)[11:16],
                color=fc,alpha=alpha,fontsize=20)

def makeImage(image,dtime,allsondes,dt_fade,col_top,col_bottom,altmax,outputfilepath):
    
    """Display GOES image, HALO circle and relevant dropsondes in their current state, and save image to outputfilepath"""

    fig = plt.figure(figsize=(20,10))
    ax = fig.gca()

    # create cmap
    cmap = LinearSegmentedColormap.from_list('mycmap', [col_bottom,col_top])

    # show frame
    h = ax.imshow(image,aspect=1)
    h.set_extent([lonmin,lonmax,latmin,latmax])

    # add circle
    circ = Circle((lon_center,lat_center),r_circle,linewidth=2,ec=col_top,fill=False)
    ax.add_patch(circ)

    # add grid
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.grid(color='w', linestyle='-', linewidth=0.5)

    # show colorbar
    x,y,w,h = ax.get_position().bounds
    c_map_ax = fig.add_axes([x+0.78*w, y+0.05*h, 0.008*w, 0.5*h])
    cbar = mpl.colorbar.ColorbarBase(c_map_ax, cmap=cmap, orientation = 'vertical')
    cbar.ax.set_ylabel('z(km)',fontsize=20,color='w') # cbar legend
    h_values = np.linspace(0,altmax,6)
    cbar.ax.set_yticklabels(['%1.1f'%(v/1000) for v in h_values],fontsize=15) # set ticklabels
    cbar.ax.tick_params(axis='y',colors='w') # set tick color in white

    # show sondes
    for sonde in getMatchingSondes(allsondes,dtime,dt_fade):
        showSonde(ax,dtime,sonde,cmap_falling=cmap,altmax=altmax)

    # show current time
    showTime(ax,dtime)

    # remove axes
    ax.xaxis.set_ticklabels([])
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticklabels([])
    ax.yaxis.set_ticks_position('none')
    
    # save and close
    plt.savefig(outputfilepath,bbox_inches='tight',dpi=120)
    plt.close()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="")
    # parser.add_argument('--date',type=str,default=None,
    #                     help="Date in format YYYY-mm-dd")
    # parser.add_argument('--time',type=str,default=None,
    #                     help="Time in format HH:MM:SS")
    # args = parser.parse_args()
    # args.dt = datetime.datetime.strptime(args.date+args.time,"%Y-%m-%d%H:%M:%S")

    # print(args)
    # print(getDropsondeFilename(args.dt))

    ##---- parameters that could be passed in argument ----##

    sondedir = '/Users/bfildier/Data/EUREC4A/Measurements/HALO'
    goesdir = '../../outputs/figures'
    outputdir = '../../outputs/movies/temp'

    # time to fade out
    dt_fade = 40 # (mn)

    # aircraft altitude
    altmax = 11000 # (m)

    # time range
    date_str = "2020-01-24"
    start_time = "10:00"
    end_time = "22:00"
    # start_time = "10:35"
    # end_time = "10:36"

    # Image box
    lonmin,lonmax = -60,-55
    dlon = lonmin-lonmax
    latmin,latmax = 11.5,15
    dlat = latmin-latmax

    # color choice
    col_top = 'g'
    col_bottom = 'y'

    # HALO circle
    lon_center, lat_center = -57.717,13.3
    lon_pt_circle, lat_pt_circle = -57.245,14.1903
    r_circle = np.sqrt((lon_pt_circle-lon_center)**2+(lat_pt_circle-lat_center)**2)

    ##---- generate images ----##

    start = datetime.datetime.strptime(date_str+start_time,'%Y-%m-%d%H:%M')
    end = datetime.datetime.strptime(date_str+end_time,'%Y-%m-%d%H:%M')
    dt = datetime.timedelta(seconds=60)
    Nt = int((end-start).seconds/60)

    print(Nt)

    # Load first image
    image = loadImage(start)
    current_image_time = imageNameRoot(start)

    # Load all sondes
    allsondes = loadSondes(start)

    for i in range(Nt):

        dtime = start + i*dt

        # update image if necessary (every 10mn)
        if imageNameRoot(dtime) != current_image_time:

            image = loadImage(dtime)
            current_image_time = imageNameRoot(dtime)

        print('make %s'%outputFileName(dtime))
        # define output file
        outputfilepath = os.path.join(outputdir,outputFileName(dtime))
        # make image
        makeImage(image,dtime,allsondes,dt_fade,col_top,col_bottom,altmax,outputfilepath)

