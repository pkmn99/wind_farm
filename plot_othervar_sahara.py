"""
Map for changes in other climate variables for sahara case
09/22/2016
Adding mean value on map
09/23
Modified for surface pressure,  relative humidity, and moisture convergence
04/02/2017
Use new wind farm stipple method 04/03
"""
import numpy as np
#import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt
from scipy import stats

import iris 
import iris.plot as iplt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from weighed_mean import get_mean 

def load_diff_data(exp_name, variable_name,nomask=False):
    # Read moisture convergence from text 
#    if variable_name == 'mconv':
#        var = iris.load('figure_data/wmask.nc')
#        var = var[0][0,:,:]
#        filename = '../' + exp_name + '_mconv.txt'
#        temp = np.loadtxt(filename)
#        temp = temp.reshape(48,96)
#	var.data = temp
#    else:
   
   # if variable_name == 'mconv':
   #     file0 = ('figure_data/%s_%s_diff_nomask.nc' % (exp_name, variable_name))
   # else:
   #     file0 = ('figure_data/%s_%s_diff.nc' % (exp_name, variable_name))
    if nomask:
        file0 = ('figure_data/%s_%s_diff_nomask.nc' % (exp_name, variable_name))
    else:
        file0 = ('figure_data/%s_%s_diff.nc' % (exp_name, variable_name))
    print "loading file " + file0
    var = iris.load(file0)
    var = var[0]
    # fix unit error in get_mean_local
    if variable_name == 'mconv':
        var.coords()[0].units='degrees'
        var.coords()[1].units='degrees'
    return var 

# Load wind mask variable
def load_wmask():
    w = iris.load('figure_data/wmask.nc')
    w = w[0][0,:,:]
    return w

# Use this to draw stiple for wind farm
def stipple(pCube, central_long=0, type='A'): 
    """ 
    Stipple points using plt.scatter for values below thresh in pCube. 
    If you have used a central_longitude in the projection, other than 0, 
    this must be specified with the central_long keyword 
    """ 
    # type 1 and 2 denote checkerboard A and B 
    if type == 'A':
        marker1 = '.'
        marker2 = 'x'
    else:
        marker1 = 'x'
        marker2 = '.'

    xOrg = pCube.coord('longitude').points 
    yOrg = pCube.coord('latitude').points 
    nlon = len(xOrg) 
    nlat = len(yOrg) 
    xData = np.reshape( np.tile(xOrg, nlat), pCube.shape ) 
    yData = np.reshape( np.repeat(yOrg, nlon), pCube.shape ) 
    sigPoints = pCube.data > 1 
    xPoints = xData[sigPoints] - central_long 
    yPoints = yData[sigPoints] 
    plt.scatter(xPoints,yPoints,s=5, c='k', marker=marker1, alpha=0.5) 

# Define contour levels and colors, taken from grads script 
def contour_color(var):
    # Defult color
    red = (np.concatenate((np.arange(15, 250, 35), np.zeros(7)+255),
                           axis=0) / 256.)
    green = np.concatenate((np.arange(15, 250, 35), 
	                    np.arange(225, 10, -35)), axis=0) / 256.
    blue = (np.concatenate((np.zeros(7)+255, np.arange(225, 10, -35)), 
                            axis=0) / 256.)

    if var=='evap':
        colors = np.array([red[2:], green[2:], blue[2:]]).T 

    if var == 'temp' or var == 'tmax' or var == 'tmin':
        colors = np.array([red[4:], green[4:], blue[4:]]).T 

    if var == 'alb':
        colors = np.array([red[1:-3], green[1:-3], blue[1:-3]]).T 

    if var == 'vegc' or var == 'sp':
        colors = np.array([red[2:], green[2:], blue[2:]]).T 

    if var == 'ssr' or var == 'gh850':
	    colors = np.array([red[3:-1], green[3:-1], blue[3:-1]]).T 

    if var == 'ws0':
	    colors = np.array([red[:-3], green[:-3], blue[:-3]]).T 

    if var == 'clc' or var == 'rh0':
	    colors = np.array([red[4:-1], green[4:-1], blue[4:-1]]).T 

    if var == 'shf':
	    colors = np.array([red[:-1], green[:-1], blue[:-1]]).T 

    if var == 'ali':
        colors = np.array([red[2:], green[2:], blue[2:]]).T 

    if var == 'mconv':
	    colors = np.array([red, green, blue]).T 

    return colors


def define_contour_level(var):
    if var == 'temp' or var == 'tmax' or var == 'tmin':
        levels = np.arange(9) - 2
    if var == 'prec' or var == 'evap':
        levels = np.arange(-2, 3.5, 0.5) 
    if var == 'alb':
        levels = np.arange(-15, 10, 3) 
    if var == 'vegc':
        levels = np.arange(-20, 31, 5) 
    if var == 'ssr':
        levels = np.arange(-30, 51, 10) 
    if var == 'clc':
        levels = np.arange(-10, 26, 5) 
    if var == 'shf':
        levels = np.arange(-30, 26, 5) 
    if var == 'ws0':
        levels = np.arange(-3, 1.6, 0.5) 
    if var == 'ali':
        levels = np.arange(-0.2, 0.31, 0.05) 
    if var == 'sp':
        levels = np.arange(-2, 3.1, 0.5) 
    if var == 'rh0':
        levels = np.arange(-5, 12.6, 2.5) 
    if var == 'mconv':
        levels = np.arange(-0.3, 0.301, 0.05) 
    if var == 'gh850':
        levels = np.arange(-12, 15.01, 3) 
    return levels 

# Grouping other variables into 3 three figures 
# group 1: alb, vegc, ali
# group 2: ssr, evap, slf
# group 3: clc, ws0
def var_group(num): 
    variable_name = ['tmax', 'tmin', 'ws0', 'alb', 'vegc', 'ssr', 'evap', 
		     'shf', 'clc','sp','rh0','mconv','gh850','gh850']
    variable_longname = [ 'Max temperature (K)',
		          'Min temperature (K)',
		          'Surface wind speed\n (m/s)',
                          'albedo (%)',
			  'Vegetation cover fraction\n (%)', 
		          'Net shortwave at surface\n (W/m2)',
			  'Evaporation (mm/day)',
			  'Sensible heat (W/m2)',
			  'Deep cloud cover (%)',
			  'Surface pressure (hPa)',
			  'Relative humidity (%)',
			  'Moisture convergence\n (g/kg s-1)',
			  'Leaf area index\n (m2/m2)',
			  'Geopotential height (m)']
    return variable_name[3*(num-1):(3*(num-1)+3)], \
	   variable_longname[3*(num-1):(3*(num-1)+3)]

def draw_var(num):
    variable_name, variable_longname = var_group(num)
    subplot_row = len(variable_name)
    exp_name = ['ExpWind0', 'ExpSolar0', 'ExpWindSolar0']	
    fig_titles = ['Wind farm', 'Solar farm', 'Wind and Solar']
    panel_label = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'] 

    wmask = load_wmask()
    levels_wmask = np.array([0, 1.1, 4.1])
    plt.figure(figsize=(12, 9))

    for i in range(subplot_row*3):
	# First three is for tempeature    
	if i < 3:
            colors = contour_color(variable_name[0])
            levels = define_contour_level(variable_name[0])
            cube = load_diff_data(exp_name[i], variable_name[0])
            mean_value1, mean_value2 = get_mean(exp_name[i], variable_name[0], 'wmask')

	if i >= 3 and i < 6:
            colors = contour_color(variable_name[1])
            levels = define_contour_level(variable_name[1])
            cube = load_diff_data(exp_name[i%3], variable_name[1])
	   # mean_value1 = get_mean_local(cube, wmask, 4)
            mean_value1, mean_value2 = get_mean(exp_name[i%3], variable_name[1], 'wmask')

	if i >= 6 and i < 9:
            colors = contour_color(variable_name[2])
            levels = define_contour_level(variable_name[2])
            cube = load_diff_data(exp_name[i%3], variable_name[2])
            mean_value1, mean_value2 = get_mean(exp_name[i%3], variable_name[2], 'wmask')

    # Make plot
        #plt.subplot(subplot_row, 3, i+1)
        plt.subplot(3, 3, i+1)

        cf = iplt.contourf(cube, levels, colors=colors, extend='both') 
        # add wind field to surface pressure
	if (num==4) & (i<=2):
            wind_u0 = load_diff_data(exp_name[i%3], 'u0',nomask=True)
            wind_v0 = load_diff_data(exp_name[i%3], 'v0',nomask=True)
            wind_ws0 = load_diff_data(exp_name[i%3], 'ws0')
            x = wind_u0.coord('longitude').points + 3.75/2 
            y = wind_u0.coord('latitude').points
            u = wind_u0.data
            v = wind_v0.data
#            plt.quiver(x, y, u, v, pivot='middle',headwidth=3,headlength=5)
            Q = plt.quiver(x, y, u, v, pivot='middle')
	    qk = plt.quiverkey(Q, 0.87, 0.91, 2, r'2m/s', labelpos='E',
	                       coordinates='figure')

	if (num==5) & (i<=2):
            wind_u850 = load_diff_data(exp_name[i%3], 'u850',nomask=True)
            wind_v850 = load_diff_data(exp_name[i%3], 'v850',nomask=True)
            wind_ws850 = load_diff_data(exp_name[i%3], 'ws850')
            x = wind_u850.coord('longitude').points + 3.75/2 
            y = wind_u850.coord('latitude').points
            u = wind_u850.data
            v = wind_v850.data
#            plt.quiver(x, y, u, v, pivot='middle',headwidth=3,headlength=5)
            Q = plt.quiver(x, y, u, v, pivot='middle')
	    qk = plt.quiverkey(Q, 0.87, 0.91, 2, r'2m/s', labelpos='E',
	                       coordinates='figure')


	plt.title(fig_titles[i%3])

        plt.gca().text(-0.12, 1.03, panel_label[i], fontsize=14, 
		       transform=plt.gca().transAxes, fontweight='bold')
        # add mean change value on map
        # give up sig and mean for mconv
	if variable_name[i/3]!='mconv': 
            plt.gca().text(0.5, 0.08,'$\Delta$:%.2f' %mean_value1, ha='center',
		           fontsize=12, color='k', transform=plt.gca().transAxes)
        plt.gca().set_xticks([-180, -120, -60, 0, 60, 120, 180])
        plt.gca().set_yticks([-90, -60, -30, 0, 30, 60, 90])
        lon_formatter = LongitudeFormatter(degree_symbol='')
        lat_formatter = LatitudeFormatter(degree_symbol='')
        plt.gca().xaxis.set_major_formatter(lon_formatter)
        plt.gca().yaxis.set_major_formatter(lat_formatter)
        plt.gca().coastlines()
        plt.gca().set_extent([-80, 80, -15, 15])

    # Add wind farm location on the map
        stipple(wmask) 
	if i%3 == 2:
   # Add axes to the figure, to place the colour bar 
   # [left, bottom, width, height]
#            c = plt.gca().get_position()
#	    print(c)
            cbar_ax = plt.gcf().add_axes([0.9125, 0.66-(0.25+0.03)*(i/3), 
		                          0.015, 0.25])  
            cbar = plt.colorbar(cf, cbar_ax, orientation='vertical')
            cbar.ax.set_ylabel(variable_longname[i/3])

#    plt.savefig('figure_othervar_sahara_%d.png' %num, dpi=300)
    plt.savefig('figure_othervar_sahara_%d.pdf' %num)
    plt.subplots_adjust(left=0.05)
    iplt.show()

def main():
#    draw_var(1)
#    draw_var(2)
#    draw_var(3)
#    draw_var(4)
    draw_var(5)

if __name__ == '__main__':
    main()
