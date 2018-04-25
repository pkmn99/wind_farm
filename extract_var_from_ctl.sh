#!/bin/bash
# This script uses grads_to_netcdf.sh to extract the desired variable in 
# the model output data from ctl format to netcdf file 
# 09/14/2016
exp=(Ctl_diurnal ExpWind0 ExpSolar0 ExpWindSolar0 ExpWindG ExpSolarG ExpWindSolarG)
#exp=(Ctl_diurnal ExpWind0 ExpSolar0 ExpWindSolar0 ExpWindG ExpSolarG ExpWindSolarG ExpWind0v)
#exp=(Ctl_diurnal ExpWind0 ExpSolar0 ExpWindSolar0 ExpWindG ExpSolarG ExpWindSolarG ExpWind0v)
#exp=(ExpWind1 ExpWind2 ExpWind3 ExpWind4 ExpSolar1 ExpSolar2 ExpSolar3 ExpSolar4)
#exp=(ExpWindf2 ExpWindf6 ExpWindf8)
#exp=(ExpWindGf2 ExpWindGf6 ExpWindGf8)
#exp=(ExpWindmosaic0 ExpWindmosaic1 ExpWind1 ExpWind2 ExpWind3 ExpWind3 ExpSolar1 ExpSolar2 ExpSolar3 Expsolar4)
#exp=(ExpSolar0 ExpSolar0v ExpWindSolar0)
#exp=(ExpSolarG ExpWindSolarG)
for i in `seq 0 6`
do
    echo processing ${exp[i]}
    ./grads_to_netcdf.sh ${exp[i]}
done

