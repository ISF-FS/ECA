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
    
    # nc = netCDF4.Dataset(url)
    # times = nc.variables['time']
    # h = nc.variables[vname]
    # jd = netCDF4.num2date(times[:],times.units)
    # import netCDF4
    # import numpy as np
    # import xarray as xr
    # import pandas as pd
    
    # f = netCDF4.Dataset("daily_data", 'r')
    
    # daily_dataset = xr.Dataset({'precipitation': (['time', 'lat', 'lon'],  f['precipitation'][:, :, :])},
    #              coords={'lat': (f['lat'][:]), 'lon': (f['lon'][:]), 'time': pd.date_range('1979-01-01', periods=9862)})
    
    # monthly_dataset = daily_dataset['precipitation'].resample('M', dim='time', how='sum', skipna=False)
 # NaN = float("nan") # Make a constant for NaN

 # def sum_nan_threshold(iterable, *, nan_threshold=10):
 #     if sum(x == NaN for x in iterable) >= nan_threshold: # Are there more NaNs then threshold?
 #         return NaN
 #     else:
 #         return sum(x for x in iterable if x != NaN) # Else sum up if not equal to NaN
    
    
    import netCDF4 as nc
    import numpy as np
    import xarray as xr
    import pandas as pd
    fn = nc.Dataset('chirps-v2.0.1981.days_p05.nc')# example for reading data
    print(fn.variables.keys()) # get all variable names
    #fn='chirps-v2.0.1981.days_p05.nc'
    print(fn)
    for dim in fn.dimensions.values():
        print(dim)    
    for var in fn.variables.values():
        print(var)   
    #print(fn['precip'])
    time_dataset=fn.variables['time'][:] 
    #print(time_dataset)
    lats = fn.variables['latitude'][:] 
    lons = fn.variables['longitude'][:]
    # latitude lower and upper index
    latli = np.argmin( np.abs( lats - lat_min ) )
    latui = np.argmin( np.abs( lats - lat_max ) ) 

    # longitude lower and upper index
    lonli = np.argmin( np.abs( lons - lon_min ) )
    lonui = np.argmin( np.abs( lons - lon_max ) )
    daily_dataset = xr.Dataset({'precip': (['time', 'latitude', 'longitude'],  fn['precip'][:, latli:latui , lonli:lonui ])},
                  coords={'latitude': (fn['latitude'][latli:latui]), 'longitude': (fn['longitude'][lonli:lonui]), 'time': pd.date_range('1980-01-01', periods=365)})
    #print(daily_dataset.sizes)
    # NaN = float("nan") # Make a constant for NaN

    # def mean_nan_threshold(iterable, *, nan_threshold=20):
    #     if mean(x == NaN for x in iterable) >= nan_threshold: # Are there more NaNs then threshold?
    #         return NaN
    #     else:
    #         return mean(x for x in iterable if x != NaN) # Else calculate the mean if not equal to NaN
       
    #monthly_dataset = daily_dataset.resample(time='D').mean('time',skipna=False)
    #print(monthly_dataset.sizes) 


    # Precipitation (latitude, longitude, time) 
    prcp_final = fn.variables['precip'][ :, latli:latui , lonli:lonui ] 
    #print(np.shape(prcp_final))
    test2=prcp_final[:,113,9]
    all_zeros2=not test2.any()
    pos_elt=prcp_final[prcp_final>0]
    arr_nan1=np.isnan(test2)
    #print(arr_nan1)
    idx_pos_elt=np.nonzero(prcp_final>0)
    #print(idx_pos_elt)
    return prcp_final
    
