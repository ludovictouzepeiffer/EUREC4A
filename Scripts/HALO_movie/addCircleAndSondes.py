import datetime
import argparse
import xarray as xr
import numpy as np
import os

def getDropsondeFilename(datetime):

    print(datetime.second)

    filename = 'D'+"{0:0>4}".format(datetime.year)+\
        "{0:0>2}".format(datetime.month)+\
        "{0:0>2}".format(datetime.day)+\
        "_"+\
        "{0:0>2}".format(datetime.hour)+\
        "{0:0>2}".format(datetime.minute)+\
        "{0:0>2}".format(datetime.second)+\
        "_PQC.nc"

    return filename



# def loadDropSondes(dt):

# def addCircle():
  

# argparse variables: sonde_file, background_sounding_file, delta_p
# values when run in repo root
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--date',type=str,default=None,
                        help="Date in format YYYY-mm-dd")
    parser.add_argument('--time',type=str,default=None,
                        help="Time in format HH:MM:SS")
    args = parser.parse_args()
    args.dt = datetime.datetime.strptime(args.date+args.time,"%Y-%m-%d%H:%M:%S")

    print(args)
    print(getDropsondeFilename(args.dt))

    # inputdir = ''
    # output_dir = 

    # 
