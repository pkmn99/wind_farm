"""
Plot checkerboard and quarter wind farm results 08/06/2017 

"""
import numpy as np
#import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt
from scipy import stats

import iris 
import iris.plot as iplt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from weighed_mean import get_mean_local 

def load_diff_data(exp_name, variable_name):
    file0 = ('figure_data/%s_%s_diff.nc' % (exp_name, variable_name))
    print "loading file " + file0
    var = iris.load(file0)
    var = var[0]
    return var 

# Load wind mask variable and modify its value 
# num indicate quarter wind farm 1-4 clockwise
def load_wmask(num):
    w = iris.load('figure_data/wmask.nc')
    w = w[0][0,:,:]
    # load moisac mask and quater mask
    if num <=2:
        filename = '../../work/WMASK/WMASK_sahara_mosaic0'
    else:
        filename = '../../work/WMASK/WMASK_sahara_' + str(num-2)
    w_0 = np.loadtxt(filename)
    w_0=w_0.reshape(48,96)
    w.data[(w_0!=4)&(w.data==4)]=-4
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

    sigPoints = pCube.data < -1 
    xPoints = xData[sigPoints] - central_long 
    yPoints = yData[sigPoints] 
    plt.scatter(xPoints,yPoints,s=5, c='k', marker=marker2, alpha=0.5) 

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

# Begin plot, 2 x 2. Row: temp, prec; Col: mosaic0 and 1
def main():
    exp_name = ['ExpWindmosaic0', 'ExpWindmosaic1', 'ExpWind1', 'ExpWind2', 'ExpWind3', 'ExpWind4']
    variable_name =['temp0', 'prec']
    fig_titles = ['Checkerboard A', 'Checkerboard B', 'Northwest',
                  'Northeast', 'Southwest', 'Southeast']
    panel_label = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    colors_temp = contour_color('temp')
    levels_temp = define_contour_level('temp')
    colors_prec = contour_color('prec')
    levels_prec = define_contour_level('prec')

    levels_wmask = np.array([0, 1.1, 4.1])
    plt.figure(figsize=(9, 7))

    for i in range(12):
    # Make plot
        plt.subplot(4, 3, i+1)
        if i < 6: 
            cube = load_diff_data(exp_name[i], variable_name[0])
            cf_temp = iplt.contourf(cube, levels_temp, colors=colors_temp, extend='both') 
        else:
            cube = load_diff_data(exp_name[i-6], variable_name[1])
            cf_prec = iplt.contourf(cube, levels_prec, colors=colors_prec, extend='both') 
        plt.title(fig_titles[i%6])

        #    plt.title(fig_titles[i-3])
#        plt.gca().text(-0.12, 1.03, panel_label[i], fontsize=14,
#                       transform=plt.gca().transAxes, fontweight='bold')
            # add mean change value on map
	if i%3 == 0:
            plt.gca().set_yticks([-90, -60, -30, 0, 30, 60, 90])
       # plt.gca().set_xticks([-180, -120, -60, 0, 30, 60, 120, 180])
        plt.gca().set_xticks([0, 30])
        lon_formatter = LongitudeFormatter(degree_symbol='')
        lat_formatter = LatitudeFormatter(degree_symbol='')
        plt.gca().xaxis.set_major_formatter(lon_formatter)
        plt.gca().yaxis.set_major_formatter(lat_formatter)
        plt.gca().coastlines()
       # plt.gca().set_extent([-80, 80, -15, 15])
        plt.gca().set_extent([-30, 60, 0, 30])


        # Add wind farm location on the map and  add text to show averaged change
        if i < 6:
            wmask = load_wmask(i+1)
	    # special case for mosaic B
	    if i==1:
                stipple(wmask,type='B') 
	    else:
		stipple(wmask) 
            mean_value1 = get_mean_local(exp_name[i%6], variable_name[0], wmask, 4)
            plt.gca().text(0.6, 0.08,'$\Delta$:%.2f' %mean_value1, ha='center',
			   fontsize=12, color='k', transform=plt.gca().transAxes)
        else:
            wmask = load_wmask(i-5)
	    # special case for mosaic B
	    if i==7:
                stipple(wmask,type='B') 
	    else:
		stipple(wmask) 
            mean_value1 = get_mean_local(exp_name[i%6], variable_name[1], wmask, 4)
           # mean_value2 = get_mean_local(cube, wmask, 4)
            plt.gca().text(0.6, 0.08,'$\Delta$:%.2f' %mean_value1, ha='center',
            		   fontsize=12, color='k', transform=plt.gca().transAxes)

   # Add axes to the figure, to place the colour bar 
    cbar_ax_temp = plt.gcf().add_axes([0.915, 0.56, 0.015, 0.35]) # [left, bottom, width, height] 
    cbar = plt.colorbar(cf_temp, cbar_ax_temp, orientation='vertical')
    cbar.ax.set_ylabel('Temperature (K)')

    cbar_ax_prec = plt.gcf().add_axes([0.915, 0.09, 0.015, 0.35]) # [left, bottom, width, height] 
    cbar = plt.colorbar(cf_prec, cbar_ax_prec, orientation='vertical')
    cbar.ax.set_ylabel('Precipitation (mm/day)')
    plt.subplots_adjust(top=0.95, bottom=0.05, left=0.05, hspace=0.15, wspace=0)
    plt.savefig('fig_checkerboard_quarter_rev.pdf')
    iplt.show()

if __name__ == '__main__':
    main()
