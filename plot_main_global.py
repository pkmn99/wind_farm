"""
Global maps for wind farm and solar panel impact
09/12/2016
Adding mean value on map
09/23
Use new stipple windfarm 04/09/2017
"""
import numpy as np
#import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt
from scipy import stats

import iris 
import iris.plot as iplt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from weighed_mean import get_mean 
from plot_othervar_sahara import stipple

# Define display range of the world
global extent
extent=[-120, 120, -40, 60]
#extent=[-140, 140, -60, 70]

def load_diff_data(exp_name, variable_name, extent):
    file0 = ('figure_data/%s_%s_diff.nc' % (exp_name, variable_name))
    print "loading file " + file0
    var = iris.load(file0)
    var = var[0]
    #var = var[0]
    var = cube_subset(var, extent)
    return var 

 #  extent = [lon1, lon2, lat1, lat2]	
def cube_subset(cube, extent):
    if extent == 'None':
        cube_new = cube
    else:
        [lon1, lon2, lat1, lat2] = extent	
        cube_new = cube.intersection(longitude=(lon1, lon2), 
			             latitude=(lat1, lat2))
    return cube_new
    
# Load wind mask variable
def load_wmask(region, extent):
    if region == 'sahara':
        w = iris.load('figure_data/wmask.nc')
    if region == 'global':
        w = iris.load('figure_data/wmask_g.nc')
    w = w[0][0,:,:]
    w = cube_subset(w, extent)
    return w

# Define contour levels and colors, taken from grads script 
def contour_color(var):
    if var == 'temp':
        red = (np.concatenate((np.arange(15, 250, 35), np.zeros(7)+255),
                               axis=0) / 256.)
        green = np.concatenate((np.arange(15, 250, 35), 
		                np.arange(225, 10, -35)), axis=0) / 256.
        blue = (np.concatenate((np.zeros(7)+255, np.arange(225, 10, -35)), 
		axis=0) / 256.)
        colors = np.array([red[4:], green[4:], blue[4:]]).T 
    if var == 'prec':
        red = np.array([116, 171, 208, 229, 242, 253, 255, 188, 140, 93, 61,
		        28, 4, 5]) /256.
        green = np.array([26, 44, 77, 126, 193, 222, 248, 230, 204, 171, 137,
		          93, 49, 24]) /256.
	blue = np.array([15, 0, 0, 3, 45, 80, 150, 243, 221, 207, 195, 166,
		         119, 64]) /256.
        colors = np.array([red[2:], green[2:], blue[2:]]).T 
    return colors


def define_contour_level(var):
    if var == 'temp':
        levels = np.arange(9) - 2
    if var == 'prec':
        levels = np.arange(-2, 3.5, 0.5) 
    return levels 

def make_plot():
    exp_name = ['ExpWindG', 'ExpSolarG', 'ExpWindSolarG']
    variable_name =['temp0', 'prec']
    fig_titles = ['Wind farm', 'Solar farm', 'Wind and Solar']
    panel_label = ['a', 'b', 'c', 'd', 'e', 'f'] 
#    extent = [-140, 140, -60, 70]
#    extent = 'None'
    wmask = load_wmask('global', extent)
    levels_wmask = np.array([0, 1.1, 4.1])
    #plt.figure(figsize=(12, 4.5), dpi=300)
#    plt.figure(figsize=(12, 4.5))
    plt.figure(figsize=(10,8))

    for i in range(6):
	print(exp_name[i/2])
	# First three is for tempeature    
	if (i%2)==0:
            colors = contour_color('temp')
            levels = define_contour_level('temp')
            cube = load_diff_data(exp_name[i/2], variable_name[0], extent)
	    mean_value1, mean_value2 = get_mean(exp_name[i/2], variable_name[0],
			                        'wmask_g')
        else:
            colors = contour_color('prec')
            levels = define_contour_level('prec')
            cube = load_diff_data(exp_name[i/2], variable_name[1], extent)
	    mean_value1, mean_value2 = get_mean(exp_name[i/2], variable_name[1],
			                        'wmask_g')
    # Make plot
        plt.subplot(3, 2, i+1)
	if (i%2)==0: 
            cf_temp = iplt.contourf(cube, levels, colors=colors, extend='both') 
	    plt.title(fig_titles[i/2])
        else:
            cf_prec = iplt.contourf(cube, levels, colors=colors, extend='both') 
	    plt.title(fig_titles[i/2])
       # plt.gca().text(-0.12, 1.03, panel_label[i], fontsize=14, 
        plt.gca().text(0, 1.03, panel_label[i], fontsize=14, 
		       transform=plt.gca().transAxes, fontweight='bold')
        # add mean change value on map
       # plt.gca().text(0.5, 0.08,'$\Delta$:%.2f' %mean_value1, ha='center',
        plt.gca().text(0.45, 0.08,'$\Delta$:%.2f' %mean_value1, ha='center',
	               fontsize=12, color='k', transform=plt.gca().transAxes)
        plt.gca().set_xticks([-180, -120, -60, 0, 60, 120, 180])
        plt.gca().set_yticks([-90, -60, -30, 0, 30, 60, 90])
        lon_formatter = LongitudeFormatter(degree_symbol='')
        lat_formatter = LatitudeFormatter(degree_symbol='')
        plt.gca().xaxis.set_major_formatter(lon_formatter)
        plt.gca().yaxis.set_major_formatter(lat_formatter)
        plt.gca().coastlines()
#	c = plt.gca().get_extent()
#	print(c)

    # Add wind farm location on the map
        stipple(wmask)

   # Add axes to the figure, to place the colour bar 
    cbar_ax_temp = plt.gcf().add_axes([0.1, 0.075, 0.35, 0.015]) # [left, bottom, width, height] 
    cbar = plt.colorbar(cf_temp, cbar_ax_temp, orientation='horizontal')
    cbar.ax.set_xlabel('Temperature (K)')

    cbar_ax_prec = plt.gcf().add_axes([0.585, 0.075, 0.35, 0.015]) # [left, bottom, width, height] 
    cbar = plt.colorbar(cf_prec, cbar_ax_prec, orientation='horizontal')
    cbar.ax.set_xlabel('Precipitation (mm/day)')

   # plt.subplots_adjust(left=0.05,right=0.95,top=0.9, bottom=0.125,hspace=0.3,wspace=0.1)
    plt.subplots_adjust(left=0.06,right=0.975,top=0.9, bottom=0.125,hspace=0.3,wspace=0.15)
    plt.savefig('fig_main_global_rev.pdf')
    iplt.show()

def main():
    make_plot()

if __name__ == '__main__':
    main()
