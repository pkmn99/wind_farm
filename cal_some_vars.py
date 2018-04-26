"""
  Summed up precipitation
  09/14/2016
  Add wind speed calculation
  09/21
  Add wind at 850 hpa
"""
import numpy as np
import numpy.ma as ma
import iris 
import iris.plot as iplt

# Sum up preclc and percls
def calculate_prec(exp_name):
    file0 = "../" + exp_name + "/precls.nc"
    file1 = "../" + exp_name + "/precnv.nc"
    print "sum up " + file0 + " and " + file1
    var0 = iris.load(file0)[0]
    var1 = iris.load(file1)[0]
    var = var1 + var0
    var.rename('Precipitation (precnv+precls)')
    iris.save(var, '../%s/prec.nc' % exp_name)
    print('file saved at ../%s/prec.nc' % exp_name)

# Calculate wind magnitude, ws0
def calculate_ws0(exp_name):
    file0 = "../" + exp_name + "/u0.nc"
    file1 = "../" + exp_name + "/v0.nc"
    print "Calculating wind speed " + file0 + " and " + file1
    var0 = iris.load(file0)[0]
    var1 = iris.load(file1)[0]
    var = np.power(var1 * var1 + var0 * var0, 0.5)
    var.rename('Surface wind speed')
    iris.save(var, '../%s/ws0.nc' % exp_name)
    print('file saved at ../%s/ws0.nc' % exp_name)

# Extract the 850 hpa wind  u and v
def calculate_wind_850(exp_name):
    file0 = "../" + exp_name + "/u.nc"
    file1 = "../" + exp_name + "/v.nc"
    print "Calculating wind speed at 850hpa"
    var0 = iris.load_cube(file0)[:,1]
    var1 = iris.load_cube(file1)[:,1]
    iris.save(var0, '../%s/u850.nc' % exp_name)
    iris.save(var1, '../%s/v850.nc' % exp_name)
    print('file saved at ../%s/' % exp_name)

# Extract the 850 hpa geopotential height
def calculate_gh850(exp_name):
    file0 = "../" + exp_name + "/gh.nc"
    print "Calculating geopotential height at 850hpa"
    var0 = iris.load_cube(file0)[:,1]
    iris.save(var0, '../%s/gh850.nc' % exp_name)
    print('file saved at ../%s/' % exp_name)

# Calculate wind speed at 850hpa
def calculate_ws850(exp_name):
    file0 = "../" + exp_name + "/u850.nc"
    file1 = "../" + exp_name + "/v850.nc"
    print "Calculating wind speed " + file0 + " and " + file1
    var0 = iris.load(file0)[0]
    var1 = iris.load(file1)[0]
    var = (var0 ** 2 + var1 ** 2) ** 0.5
   # var = np.power(var1 * var1 + var0 * var0, 0.5)
    var.rename('wind speed at 850hpa')
    iris.save(var, '../%s/ws850.nc' % exp_name)

def save_prec(exp_name):
#    exp_name = ['Ctl_diurnal', 'ExpWind0', 'ExpSolar0', 'ExpWindSolar0', 
#		 'ExpWindG', 'ExpSolarG', 'ExpWindSolarG', 'ExpWind0v']
#    exp_name = ['ExpWindf2', 'ExpWindf6', 'ExpWindf8']
#    exp_name = ['ExpWindGf2', 'ExpWindGf6', 'ExpWindGf8']
#    exp_name = ['ExpWindmosaic0', 'ExpWindmosaic1']
    for e in range(len(exp_name)):
        calculate_prec(exp_name[e])

def save_ws0(exp_name):
    for e in range(len(exp_name)):
        calculate_ws0(exp_name[e])

def save_wind_850(exp_name):
#    exp_name = ['ExpWindf2', 'ExpWindf6', 'ExpWindf8']
#    exp_name = ['ExpWindGf2', 'ExpWindGf6', 'ExpWindGf8']
#    exp_name = ['ExpWindmosaic0', 'ExpWindmosaic1']
    for e in range(len(exp_name)):
        calculate_wind_850(exp_name[e])

# First calculate wind 850
def save_ws850(exp_name):
    for e in range(len(exp_name)):
        calculate_ws850(exp_name[e])

def save_gh850(exp_name):
    for e in range(len(exp_name)):
        calculate_gh850(exp_name[e])

def main():
#    exp=['ExpWindmosaic0', 'ExpWindmosaic1', 'ExpWind1', 'ExpWind2', 'ExpWind3',
#         'ExpWind4', 'ExpSolar1', 'ExpSolar2', 'ExpSolar3', 'Expsolar4']
#    exp=['ExpSolarG','ExpWindSolarG']
#    save_ws0(exp_name=exp)
#    save_prec(exp_name=exp)
    exp = ['Ctl_diurnal', 'ExpWind0', 'ExpSolar0', 'ExpWindSolar0', 
		 'ExpWindG', 'ExpSolarG', 'ExpWindSolarG']
#    save_wind_850(exp_name=exp)
#    save_ws850(exp_name=exp)
    save_gh850(exp_name=exp)

if __name__ == '__main__':
    main()
