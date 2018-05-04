"""
Global maps for wind farm and solar panel impact
09/12/2016
Adding mean value on map
09/23
# update with wind farm stipple scheme 04/08/2017
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

def load_diff_data(exp_name, variable_name):
    file0 = ('figure_data/%s_%s_diff.nc' % (exp_name, variable_name))
    print "loading file " + file0
    var = iris.load(file0)
    var = var[0]
    return var 

def load_diff_data_nomask(exp_name, variable_name):
    file0 = ('figure_data/%s_%s_diff_nomask.nc' % (exp_name, variable_name))
    print "loading file " + file0
    var = iris.load(file0)
    var = var[0]
    return var 

# Load wind mask variable
def load_wmask():
    w = iris.load('figure_data/wmask.nc')
    w = w[0][0,:,:]
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

def main():
    exp_name = ['ExpWind0', 'ExpSolar0', 'ExpWindSolar0']	
    variable_name =['temp0', 'prec']
    fig_titles = ['Wind farm', 'Solar farm', 'Wind and Solar']
    panel_label = ['a', 'b', 'c', 'd', 'e', 'f'] 

    wmask = load_wmask()
    levels_wmask = np.array([0, 1.1, 4.1])
    plt.figure(figsize=(7, 8.5))

    for i in range(6):
	# First three is for tempeature    
	if (i%2)==0:
            colors = contour_color('temp')
            levels = define_contour_level('temp')
            cube = load_diff_data(exp_name[i/2], variable_name[0])
	    mean_value1, mean_value2 = get_mean(exp_name[i/2], variable_name[0],
			                        'wmask')
        else:
            colors = contour_color('prec')
            levels = define_contour_level('prec')
            cube = load_diff_data(exp_name[i/2], variable_name[1])
	    mean_value1, mean_value2 = get_mean(exp_name[i/2], variable_name[1],
			                        'wmask')
    # Make plot
        plt.subplot(3, 2, i+1)
	if (i%2)==0:
            cf_temp = iplt.contourf(cube, levels, colors=colors, extend='both') 
	    plt.title(fig_titles[i/2])
        else:
            cf_prec = iplt.contourf(cube, levels, colors=colors, extend='both') 
	    plt.title(fig_titles[i/2])
        plt.gca().text(-0.12, 1.03, panel_label[i], fontsize=14, 
		       transform=plt.gca().transAxes, fontweight='bold')
        # add mean change value on map
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

   # Add axes to the figure, to place the colour bar 
    cbar_ax_temp = plt.gcf().add_axes([0.1, 0.075, 0.35, 0.0125]) # [left, bottom, width, height] 
    cbar = plt.colorbar(cf_temp, cbar_ax_temp, orientation='horizontal')
    cbar.ax.set_xlabel('Temperature (K)')

    cbar_ax_prec = plt.gcf().add_axes([0.585, 0.075, 0.35, 0.0125]) # [left, bottom, width, height] 
    cbar = plt.colorbar(cf_prec, cbar_ax_prec, orientation='horizontal')
    cbar.ax.set_xlabel('Precipitation (mm/day)')
    plt.subplots_adjust(hspace=0.1, left=0.075, right=0.95, top=0.95)

    plt.savefig('fig_main_sahara_rev.pdf')
    iplt.show()

if __name__ == '__main__':
    main()
