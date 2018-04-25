"""
* Conduct two smaple T-test on the difference of Exp and Ctl is significant
  at 0.05. And save the difference and p-vale of each variable to local file, which
  will be used to plot figure
  09/14/2016
* Add vegon option to enable separating the vegtation feedback 09/20
* Use summed up precipiation before t-test
  09/23
* Add nomask difference  
* Modified exp_ctl_diff to avoid segmentation bug for prec 11/01

!!! Must run cal_some_vars.py to get prec and ws0 before using this
"""
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from scipy import stats

import iris 
import iris.plot as iplt

def t_test_2d_1samp(data_3d):
    p = np.zeros([data_3d.shape[1], data_3d.shape[2]])
    for lat in range(data_3d.shape[1]): 
        for lon in range(data_3d.shape[2]): 
		temp = data_3d[:, lat, lon]  
                result = stats.ttest_1samp(temp.data, 0)
                p[lat, lon] = result.pvalue 
    return p

def t_test_2d_2samp(data_3d, data_3d2):
    p = np.zeros([data_3d.shape[1], data_3d.shape[2]])
    for lat in range(data_3d.shape[1]): 
        for lon in range(data_3d.shape[2]): 
		temp = data_3d[:, lat, lon]  
		temp2 = data_3d2[:, lat, lon]  
                result = stats.ttest_ind(temp.data, temp2.data)
                p[lat, lon] = result.pvalue 
    return p

# Load experiment data and compute its difference with control 
# run for ttest
def load_data(exp_name, variable_name, vegon=0):
    if vegon ==0:
        file0 = "../Ctl_diurnal/" + variable_name + ".nc"
        file1 = "../" + exp_name + "/" + variable_name + ".nc"
    else: 
        file0 = "../" + exp_name +"/" + variable_name + ".nc"
	file1 = "../" + exp_name[:-1] +"/" + variable_name + ".nc"
    print "load " + file0
    print "load " + file1
    var0 = iris.load(file0)
    var0 = var0[0]
    var1 = iris.load(file1)
    var1 = var1[0]
    return var0, var1 

#   Exp - Ctl 
def exp_ctl_diff(exp_name, variable_name, vegon=0):
    if vegon == 0:
        data0, data1 = load_data(exp_name, variable_name)
    else:
        data0, data1 = load_data(exp_name, variable_name, vegon=1)
    data0_mean = data0.collapsed('time', iris.analysis.MEAN)
    data1_mean = data1.collapsed('time', iris.analysis.MEAN)
#    diff_mean = data1_mean - data0_mean
    # Fix for subtraction issue
    diff_mean = data0_mean
    diff_mean.data = data1_mean.data - data0_mean.data
    #print 'type of diff_mean is ', type(diff_mean.data)
    p = t_test_2d_2samp(data0, data1)
    # create a mask for p-value > 0.05
    p_mask = np.logical_or(p > 0.05, np.isnan(p)) 
    diff_mean.data = ma.array(diff_mean.data, mask=p_mask)
    #print 'type of diff_mean is ', type(diff_mean.data)
    if vegon == 0:
        diff_mean.rename('Difference of %s' % variable_name)
        iris.save(diff_mean, 'figure_data/%s_%s_diff.nc'
                  % (exp_name, variable_name))
        print 'figure_data/%s_%s_diff.nc saved' % (exp_name, variable_name)
    else:
        diff_mean.rename('Difference of %s, vegon' % variable_name)
        iris.save(diff_mean, 'figure_data/%s_%s_diff_veg.nc'
                  % (exp_name, variable_name))
        print 'figure_data/%s_%s_diff_veg.nc saved' % (exp_name, variable_name)
#    iplt.pcolormesh(diff_mean)
#    iplt.show()

def exp_ctl_diff_nomask(exp_name, variable_name, vegon=0):
    if vegon == 0:
        data0, data1 = load_data(exp_name, variable_name)
    else:
        data0, data1 = load_data(exp_name, variable_name, vegon=1)
    data0_mean = data0.collapsed('time', iris.analysis.MEAN)
    data1_mean = data1.collapsed('time', iris.analysis.MEAN)
   # diff_mean = data1_mean - data0_mean
    # Try to fix the laitude subtraction issue
    diff_mean = data0_mean
    diff_mean.data = data1_mean.data - data0_mean.data
    #print 'type of diff_mean is ', type(diff_mean.data)
    if vegon == 0:
        diff_mean.rename('Difference of %s' % variable_name)
        iris.save(diff_mean, 'figure_data/%s_%s_diff_nomask.nc'
                  % (exp_name, variable_name))
        print 'figure_data/%s_%s_diff_nomask.nc saved' % (exp_name, variable_name)
    else:
        diff_mean.rename('Difference of %s, vegon' % variable_name)
        iris.save(diff_mean, 'figure_data/%s_%s_diff_veg_nomask.nc'
                  % (exp_name, variable_name))
        print 'figure_data/%s_%s_diff_veg_nomask.nc saved' % (exp_name, variable_name)

# Save difference with significant mask
def save_diff_mask(exp_name):
#    exp_name = ['ExpWind0', 'ExpSolar0', 'ExpWindSolar0', 'ExpWindG', 
#		'ExpSolarG', 'ExpWindSolarG', 'ExpWind0v']
#    exp_name = ['ExpWind1', 'ExpWind2', 'ExpWind3', 'ExpWind4',
#		'ExpSolar1', 'ExpSolar2', 'ExpSolar3', 'ExpSolar4']
#    exp_name = ['ExpWindGf2', 'ExpWindGf6', 'ExpWindGf8']

#    variable_name = ['tmax', 'tmin', 'temp0', 'prec', 'alb', 'vegc',
#                     'evap', 'ssr', 'ws0', 'shf', 'clc', 'clstr', 'ali']
    variable_name = ['u850', 'v850','ws850']
#    variable_name = ['tmax', 'tmin', 'temp0', 'prec', 'alb', 'vegc',
#                     'evap', 'ssr', 'ws0', 'shf', 'clc', 'clstr', 'ali', 
#                     'sp', 'rh0']
    for e in range(len(exp_name)):
        for v in range(len(variable_name)):
       # for v in range(13):
            exp_ctl_diff(exp_name[e], variable_name[v])
    #if it is ExpWind0, run one more time to get vegtation feedback 
    # for wind farm in Sahara 
	if exp_name[e] in ['ExpWind0v', 'ExpSolar0v']:
            for v in range(len(variable_name)):
                exp_ctl_diff(exp_name[e], variable_name[v], vegon=1)


# Save difference without significant mask
def save_diff_nomask(exp_name):
    print 'Saving difference without significant mask'
    
#    exp_name = ['ExpWind0', 'ExpSolar0', 'ExpWindSolar0', 'ExpWindG', 
#		'ExpSolarG', 'ExpWindSolarG', 'ExpWind0v']
#    exp_name = ['ExpWindf2', 'ExpWindf6', 'ExpWindf8']
#    exp_name = ['ExpWindGf2', 'ExpWindGf6', 'ExpWindGf8']
#    variable_name = ['tmax', 'tmin', 'temp0', 'prec', 'alb', 'vegc',
#                     'evap', 'ssr', 'ws0', 'shf', 'clc', 'clstr', 'ali',
#                     'sp', 'rh0']
#    variable_name = ['temp0']
    variable_name = ['u850', 'v850','ws850']
    for e in range(len(exp_name)):
       # for v in range(3):
        for v in range(len(variable_name)):
            exp_ctl_diff_nomask(exp_name[e], variable_name[v])
    #if it is ExpWind0, run one more time to get vegtation feedback 
    # for wind farm in Sahara 
	if exp_name[e] in ['ExpWind0v', 'ExpSolar0v']: 
            for v in range(len(variable_name)):
                exp_ctl_diff_nomask(exp_name[e], variable_name[v], vegon=1)

def main():
   # exp=['ExpWindSolar0', 'ExpSolar0']
#    exp=['ExpSolarG', 'ExpWindSolarG']
#    exp=['ExpWindmosaic1', 'ExpWind1', 'ExpWind2', 'ExpWind3',
#         'ExpWind3', 'ExpSolar1', 'ExpSolar2', 'ExpSolar3', 'Expsolar4']
    exp = ['ExpWind0', 'ExpSolar0', 'ExpWindSolar0', 'ExpWindG', 
		'ExpSolarG', 'ExpWindSolarG'] #, 'ExpWind0v']
    save_diff_mask(exp_name=exp)
    save_diff_nomask(exp_name=exp)
#    exp = ['ExpWind0', 'ExpSolar0', 'ExpWindSolar0', 'ExpWindG',
#	   'ExpSolarG', 'ExpWindSolarG']
#    save_diff_nomask(exp_name=exp)
if __name__ == '__main__':
    main()
