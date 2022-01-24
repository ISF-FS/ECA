# -*- coding: utf-8 -*-
"""
%%Can Tho city Vietnam Heatwave Hazard creation.

@author: daou
"""

# setting points
import numpy as np
from scipy import sparse
from itertools import product
import pandas as pd

lon_min = 105.665281;
lon_max = 105.845963;
lat_min =  9.954246;
lat_max =  10.117987;

# lat = np.array([26.933899, 26.957203, 26.783846, 26.645524, 26.897796, 26.925359, \
#        26.914768, 26.853491, 26.845099, 26.82651 , 26.842772, 26.825905, \
#        26.80465 , 26.788649, 26.704277, 26.71005 , 26.755412, 26.678449, \
#        26.725649, 26.720599, 26.71255 , 26.6649  , 26.664699, 26.663149, \
#        26.66875 , 26.638517, 26.59309 , 26.617449, 26.620079, 26.596795, \
#        26.577049, 26.524585, 26.524158, 26.523737, 26.520284, 26.547349, \
#        26.463399, 26.45905 , 26.45558 , 26.453699, 26.449999, 26.397299, \
#        26.4084  , 26.40875 , 26.379113, 26.3809  , 26.349068, 26.346349, \
#        26.348015, 26.347957])

# lon = np.array([-80.128799, -80.098284, -80.748947, -80.550704, -80.596929, \
#        -80.220966, -80.07466 , -80.190281, -80.083904, -80.213493, \
#        -80.0591  , -80.630096, -80.075301, -80.069885, -80.656841, \
#        -80.190085, -80.08955 , -80.041179, -80.1324  , -80.091746, \
#        -80.068579, -80.090698, -80.1254  , -80.151401, -80.058749, \
#        -80.283371, -80.206901, -80.090649, -80.055001, -80.128711, \
#        -80.076435, -80.080105, -80.06398 , -80.178973, -80.110519, \
#        -80.057701, -80.064251, -80.07875 , -80.139247, -80.104316, \
#        -80.188545, -80.21902 , -80.092391, -80.1575  , -80.102028, \
#        -80.16885 , -80.116401, -80.08385 , -80.241305, -80.158855])
# create meshgrid
[X, Y ] = np.meshgrid(np.linspace(lon_min,lon_max,1975), np.linspace(lat_min,lat_max,1806))
n_cen = lon.size # number of centroids
n_ev = 5 # number of events


def ev_name(string):
    #string = input("string: ")
    f_name=[]
    counter=0
    num_digits = string.count("%d")    #Example: 'Somali%d%d' or 'HND%d'
    if num_digits > 0:
      digit_str = string.replace("%d", "{}")
      for digits in product("12345", repeat=num_digits):  
            ev_name=digit_str.format(*digits)
            out1=[ev_name]
            if counter==0:
                out=[f_name, ev_name]
            elif counter==-1:
                f_name=out[-1]
                out = [f_name, ev_name]
            else:
                f_name= out+out1
                out=f_name  
            counter=counter-1
    return f_name
 
#evt_name=ev_name('Somali%d%d') 

        

haz = Hazard('HW')

lon = np.reshape(X, (np.product(X.shape,)) 
lat = np.reshape(Y, -1, order='F') 

haz.centroids = Centroids.from_lat_lon(lat, lon) # default crs used
haz.intensity = sparse.csr_matrix(np.random.random((n_ev, n_cen)))
haz.units = 'no_unit'
haz.event_id = np.arange(n_ev, dtype=int)
haz.event_name = ev_name('CanThoHW%d')
#haz.event_name = ['ev_12', 'ev_21', 'Maria', 'ev_35', 'Irma', 'ev_16', 'ev_15', 'Edgar', 'ev_1', 'ev_9']
#haz.date = [721166, 734447, 734447, 734447, 721167, 721166, 721167, 721200, 721166, 721166]
tdate=[2020]
haz.date=np.repeat(tdate, repeats = [n_ev], axis=0)
haz.orig = np.zeros(n_ev, bool)
haz.frequency = np.ones(n_ev)/n_ev
haz.fraction = haz.intensity.copy()
haz.fraction.data.fill(1)

hazard.lon = np.reshape(X, (np.product(X.shape,)) #reshape through rows
hazard.lat = np.reshape(Y, -1, order='F') # reshape through columns
haz.check()
haz.centroids.plot()