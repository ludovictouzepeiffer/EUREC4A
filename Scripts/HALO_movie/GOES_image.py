"""
Script to download images from NASA Worldview
"""
import urllib.request
import datetime
from calendar import monthrange
import fire
import os

#lon,lat,debut, fin, pas de temps, resolution, varid

https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2020-01-24T17:20:00Z&BBOX=12.310710570845181,-59.77875762732572,13.879946623093044,-57.244871330630964&CRS=EPSG:4326&LAYERS=GOES-East_ABI_Band2_Red_Visible_1km,Reference_Labels,Reference_Features&WRAP=x,x,x&FORMAT=image/jpeg&WIDTH=1153&HEIGHT=714&ts=1580766913339
                
https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2020-02-04T12:50:00Z&BBOX=11.590295139568504,-60.06121763750723,15.012647303659342,-55.119001003028224&CRS=EPSG:4326&LAYERS=GOES-East_ABI_Band2_Red_Visible_1km,Reference_Features,Reference_Labels&WRAP=x,x,x&FORMAT=image/jpeg&WIDTH=1125&HEIGHT=779&ts=3636363636336                
                
                
https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2020-02-04T12:50:00Z&BBOX=11.590295139568504,-60.06121763750723,15.012647303659342,-55.119001003028224&CRS=EPSG:4326&LAYERS=GOES-East_ABI_Band2_Red_Visible_1km,Reference_Features,Reference_Labels&WRAP=x,x,x&FORMAT=image/jpeg&WIDTH=1125&HEIGHT=779&ts=1580823288926

def download_imgs(year, month, date, time, save_path, lon_range, lat_range,
                  deg2pix=1000, satellite='Aqua', exist_skip=False, var='CorrectedReflectance_TrueColor'):
    os.makedirs(save_path, exist_ok=True)

    lon1 = lon_range[0]; lon2 = lon_range[1]
    lat1 = lat_range[0]; lat2 = lat_range[1]
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    loc= (f'&extent={lon1},{lat1},{lon2},{lat2}')
    loc_str = f'_{lon1}-{lon2}_{lat1}-{lat2}'
    size = (f'&width={int(dlon * deg2pix)}&height={int(dlat * deg2pix)}')
    layer = (f'&layers=MODIS_{satellite}_{var},Coastlines')

    date = datetime.datetime(year, month, date)
    d = str(date.strftime('%j'))
    print(date.strftime('%y %m %d'))
    url = ('https://gibs.earthdata.nasa.gov/image-download?TIME='+
                       str(year)+d+loc+'&epsg=4326'+layer+
                       '&opacities=1,1&worldfile=false&format=image/jpeg'+
                       size)
    lat_min = 11.5
    lat_max = 15
    lon_min = -60
    lon_max = -55
    width = 1125
    height = width*(lat_max-lat_min)/(lon_max-lon_min)
    
    lon_lat = lat_min+','+lon_min+'lat_max'+','+'lon_max'
    
    url = ('https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME='+date+'&BBOX'+lon_lat+'LAYERS=GOES-East_ABI_Band2_Red_Visible_1km,Reference_Labels,Reference_Features&WRAP=x,x,x&FORMAT=image/jpeg&WIDTH='+width+'&HEIGHT='+height+'&ts=1580766913339')
           
    save_str = (save_path+f'/{satellite}_CorrectedReflectance'+str(year)+
                    date.strftime('%m')+'{:02d}'.format(date.day)+str(time)+loc_str+
                    '.jpeg')
    if exist_skip and os.path.exists(save_str):
        print('Skip')
    else:
        try:
            urllib.request.urlretrieve(url, save_str)
        except:
            print(f'Download failed for {save_str}')


if __name__ == '__main__':
    fire.Fire(download_imgs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Builds a netCDF file suitable for computing radiative fluxes by merging a background sounding a sonde file from Aspen")
    parser.add_argument("--sonde_file", type=str, default="input/HALO/20200119/AVAPS_Dropsondes/processed/D20200119_161410_PQC.nc",
                        help="Name of sonde file")
    parser.add_argument("--background_file", type=str, default='tropical-atmosphere.nc',
                        help="Directory where reference values are")
    parser.add_argument("--deltaP", type=int, default=100,
                        help="Pressure discretization of sonde (Pa, integer)")
    parser.add_argument("--sfc_emissivity", type=float, default=0.98, dest="emis",
                        help="Surface emissivity (spectrally constant)")
    parser.add_argument("--sfc_albedo", type=float, default=0.07, dest="alb",
                        help="Surface albedo (spectrally constant, same for direct and diffuse)")
    parser.add_argument("--cos_sza", type=float, default=0, dest="mu0",
                        help="Cosine of solar zenith angle, default is to compute from sonde file (someday)")
    args = parser.parse_args()

    # Generalize this
    output_dir      = '.'
    output_file     = os.path.basename(args.sonde_file)[:-3] + "_rad.nc"

    # Any error checking on arguments?

    profile = combine_sonde_and_background(args.sonde_file, args.background_file, \
                                           deltaP=args.deltaP, sfc_emis=args.emis, sfc_alb=args.alb, mu0=args.mu0)
    profile.to_netcdf(os.path.join(output_dir, output_file))

'''#     for yr in range(year_range[0], year_range[1]):
#         for m in months:
#             nday = monthrange(yr,m)[1]
#             for nd in range(1,nday+1):
#                 date = datetime.datetime(yr, m, nd)
#                 d = str(date.strftime('%j'))
#                 print(date.strftime('%y %m %d'))
#                 url = ('https://gibs.earthdata.nasa.gov/image-download?TIME='+
#                        str(yr)+d+loc+'&epsg=4326'+layer+
#                        '&opacities=1,1&worldfile=false&format=image/jpeg'+
#                        size)
#                 save_str = (save_path+f'/{satellite}_CorrectedReflectance'+str(yr)+
#                     date.strftime('%m')+'{:02d}'.format(date.day)+loc_str+
#                     '.jpeg')
#                 if exist_skip and os.path.exists(save_str):
#                     print('Skip')
#                 else:
#                     try:
#                         urllib.request.urlretrieve(url, save_str)
#                     except:
#                         print(f'Download failed for {save_str}')'''

    
