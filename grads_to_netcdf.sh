#!/bin/bash
# Using cdo to convert grads data to netcdf and extract some variables
# 09/12/2016
# Usage: grads_to_netcdf.sh path_of_folder
# Example: grads_to_netcdf.sh Ctl_dirunal 
# Need to 'module load cdo'
path=$1
cd ../${path}

#infile=attmexp
#var=(tmax tmin temp0 precls precnv alb vegc evap ssr shf clc clstr u0 v0 ali)
#var=(tmax tmin temp0 precls precnv alb vegc evap ssr shf clc clstr u0 v0 ali sp rh0)
#var=(sp rh0)
#var=(ali u v)

infile=vegemo
var=(f1 f2 f3 f4)

# Convert ctl to netcdf
echo Converting ${infile}.ctl to ${infile}.nc
cdo -f nc import_binary ${infile}.ctl ${infile}.nc 
echo Conversion Done

# Subseting variables
#for i in `seq 0 16`
for i in `seq 0 3`
do
    echo Subsetting ${var[i]}
    cdo selname,${var[i]} ${infile}.nc ${var[i]}.nc 
done

echo Finish subseting
echo Deleting ${infile}.nc 
rm -f ${infile}.nc
echo All done
