# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 21:00:05 2022

@author: daou
"""

def read_cut_CHIRPS_data(lat_min,lat_max, lon_min, lon_max):
#' @details
#' Data description at 
#' \url{https://data.chc.ucsb.edu/products/CHIRPS-2.0/README-CHIRPS.txt}
#' 
#' \bold{resolution}: numeric, resolution of CHIRPS tiles either 
#'  0.05 (default) or 0.25 degrees
# this code reads precipitation netcdf files from CHIRPS data, and then cut the data based
# on the region selected, in our case it is Ethiopia Afar or Ethiopia Somali, one will need to enter
# 4 values, minimum and maximum latitude, and same for longitude
# one needs to provide 4 values (lat_min, lat_max, lon_min, lon_max) so this function works (see example below for Afar)
    #lat_min=8.8333
    #lat_max=14.533
    #lon_min=39.65
    #lon_max=42.4
# and Somali
    #lat_min=3.233833;
    #lat_max=11.0833;
    #lon_min=39.0833;
    #lon_max=47.9667;   
    
    import netCDF4 as nc
    import numpy as np
    fn = nc.Dataset('chirps-v2.0.1981.01.days_p05.nc') # example for reading data
    print(fn.variables.keys()) # get all variable names
    #fn='chirps-v2.0.1981.days_p05.nc'
    print(fn)
    #ds = xr.open_dataset(fn)
    for dim in fn.dimensions.values():
        print(dim)    
    for var in fn.variables.values():
        print(var)   
    print(fn['precip'])

    lats = fn.variables['latitude'][:] 
    lons = fn.variables['longitude'][:]

    # latitude lower and upper index
    latli = np.argmin( np.abs( lats - lat_min ) )
    latui = np.argmin( np.abs( lats - lat_max ) ) 

    # longitude lower and upper index
    lonli = np.argmin( np.abs( lons - lon_min ) )
    lonui = np.argmin( np.abs( lons - lon_max ) )  

    # Precipitation (latitude, longitude, time) 
    prcp_final = fn.variables['precip'][ :, latli:latui , lonli:lonui ] 
    print(np.shape(prcp_final))
    return prcp_final
    