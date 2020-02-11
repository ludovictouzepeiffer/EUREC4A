#
#!/bin/sh
#

#monStr="jan"
#mon="01"
#daylist="18 19 20 21 22 23 24 25 26 27 28 29 30 31"

# for day in ${daylist} ; do
 ##
#  ncl plot_WeatherStation.ncl dayStr=\"${day}\" mon=\"${mon}\" monStr=\"${monStr}\"
 ##
# done

monStr="feb"
mon="02"
daylist="02"

 for day in ${daylist} ; do
 ##
  ncl plot_WeatherStation.ncl dayStr=\"${day}\" mon=\"${mon}\" monStr=\"${monStr}\"
 ##
 done


