#!/bin/bash

#by Ludovic Touze-Peiffer
#Download data from the nas server and put them in a Data_local

daylist=(20200124 20200126 20200128 20200130 20200131 20200202 20200205 20200207 20200209)

cd ../../Data_local/Measurements/HALO/

for iday in {8..8} ; do
	
	day=${daylist[iday]}

	echo ${day}

	mkdir -p ${day}/AVAPS_Dropsondes/

	cd ${day}/AVAPS_Dropsondes/
	
	rm -rf *	

	smbget -R smb://nas.eurec4a.eu/EUREC4A/Measurements/HALO/${day}/AVAPS_Dropsondes -U eurec4a%eurec4a@EUREC4A

	cd ../../
	
done


