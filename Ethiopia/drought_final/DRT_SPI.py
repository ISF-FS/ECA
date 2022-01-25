# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 20:57:34 2022

@author: daou
"""

def SPI_G(prcp_3DArr,scale,number_of_seasons):
#This Drought Module is part of CLIMADA, but can also run as a standalone code

#Copyright (C) 2021 UNU-EHS Bonn and MCII, Listed Authors are the following:
#David Daou:                      david.daou@gmail.com
#Maxime Souvignet:                Souvignet@ehs.unu.edu
#Florian Waldschmidt:             Waldschmidt@ehs.unu.edu
#Eike Behre:                      Behre@ehs.unu.edu
#Alvaro Rojas:                    Rojas@ehs.unu.edu
#Teresa de Jesus Arce-Mojica:     Arce-Mojica@ehs.unu.edu
#Preeti Koirala:                  Koirala@ehs.unu.edu
#Irfan Ullah:                     Ullah@ehs.unu.edu

#Drought module same as CLIMADA is free software: you can redistribute it and/or modify it under the
#terms of the GNU General Public License as published by the Free
#Software Foundation, version 3.

#This module is distributed hoping it will be useful, but WITHOUT ANY
#WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#PARTICULAR PURPOSE.  See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along
#with this drought module or with CLIMADA. If not, see <https://www.gnu.org/licenses/>.

#---
#Description
#This module can calculate the following drought indices, but can also run as a model for SPI
#it works with 1D or 3D data, for some indices one will need more than one type of data (for example Precipitation and Temperature in the case of SPEI), 
#if no sufficient data is provided, the code will exit returning an error.
#+---------+-----------------------------------------------------+---------------------------+---------------------------------+----------------------------+---------------------------+
#| Acronym | Name                                                | Advantages                | Limitation                      | Drought type               | Data Needed               |
#+---------+-----------------------------------------------------+---------------------------+---------------------------------+----------------------------+---------------------------+
#| SPI_G   | Standard Precipitation Index  Gamma distribution    | low data requirement      | do not consider temperature     | Meteorological             | Precipitation             |
#|         |                                                     | easy to compute           | needs a distribution selection  | Hydrological, Agricultural |                           |                                                     | Global                    |          |
#+---------+-----------------------------------------------------+---------------------------+---------------------------------+----------------------------+---------------------------+
#| SPI_P   | Standard Precipitation Index Polynomial Distribution| same as above             | same as above                   | same as above              | Precipitation             |
#+---------+-----------------------------------------------------+---------------------------+---------------------------------+----------------------------+---------------------------+

#Finally this code works well on monthly precipitation data for more than 20 years, to give good results, We will be 
# writing a function to convert daily data to monthly in a future release

#20/01/2022 version 0.0.1
#Start Importing.
#"""

    import numpy as np
    from scipy.stats import gamma
    from scipy import stats
    ##test on calculation of SPI (Standardized Precipitation Index)    
    # this code calculates the SPI for drought using the gamma distribution,or a polynomial function
    # this code works if the input is a matrix (3D array)
    # based on the literature, we need at least 20 years of data for this code
    # to give good results.
    # if we've been passed a 2D array raise an error and if it's a 3D array
    # then we flatten it, otherwise raise an error
    shape = prcp_3DArr.shape
    #load prec
    precip_data = prcp_3DArr
    # the next few lines can be commented for now, but we will be using them in a future version
    if len(shape) == 3:
        prcp_3DArr = prcp_3DArr.flatten()
    elif len(shape) != 1:
        message = "wrong size of input array: {shape}".format(shape=shape) + \
                  " -- only 3D flattened arrays to 1D array are supported"
        _logger.error(message)
        raise ValueError(message)
    # Set all the Fill Value (missing values) from the netcdf file as NaN
    precip_data[precip_data== 9.969209968386869e+36]=np.nan
    precip_data[precip_data== -9999.0]=np.nan


    # Set all negative values to zero
    if np.amin(precip_data) < 0.0:
        _logger.warning("Input array contains negative values -- all negatives values are set to zero")
        precip_data = np.clip(precip_data, a_min=0.0, a_max=None)    
   

   

    
    # record the size of the original 3D array
    original_size = precip_data.size


    size_row = np.size(precip_data, 0)
    size_col = np.size(precip_data, 1)

    erase_yr = np.ceil(scale / 12)
    precip_data=np.transpose(precip_data, (2,1,0)) 
    size_row1 =precip_data.shape[0]
    size_col1 =precip_data.shape[1]
    size_3rd1 =precip_data.shape[2]

    ## a for loop to compute the SPI for each grid
    SPI= np.array([])

    SPI_FINAL= np.zeros([size_row1,size_col1,size_3rd1])
    for n in range(0,size_row1):
        for m in range(0,size_col1):
            loop_data = np.stack(precip_data[n,m,:], axis=0)

            scaled_data = np.array([])
            for i in range(0,scale):
                length_loop_data=len(loop_data)
                test=loop_data[i:length_loop_data-scale+i]
                if i==0:
                    scaled_data =test 
                else :
                    scaled_data = np.column_stack((scaled_data, test))
                
            scaled_data=np.array(scaled_data).T

            # do the sum along the columns (for example line 1 and columns from 1 to end)
            sum_sc_d = np.sum(scaled_data, axis=0)

            #sum_sc_d =scaled_data.sum(axis=0)
            # we will use the gamma distribution which is defined by its frequency to
            # calculate the SPI, and this is based on several papers in the literature
            # among these papers (Mckee et all(1993) (USA), Shah et al (2015) (India), Guenang &
            # Kamga (2014) (Cameroon), Gidey et al (2018) (Ethiopia).
            # Gamma defined as G(x)=
            # (1/(Beta*exp.alpha*Tau*exp.alpha))*(x*exp(alpha-1))*(e*exp(-x/beta))
            # alpha and beta are both strictly positive, x>0, and alpha being the shape
            # parameter and beta the scale parameter and x the amount of rainfall
            # from the maximum likelihood solutions based on Thom(1966)
            # A=ln(mean(x))-sum(ln(x))/n and alpha=(1/4A)*(1+sqrt(1+4*A/3))
            # and beta= mean(x)/alpha; where n is the number of precipitation
            # observations.

            if (scale > 1):
                sum_sc_d[1:int(number_of_seasons * erase_yr - scale + 2)] = []
            size_scaled_data = np.asarray(sum_sc_d).size
            for i in range(number_of_seasons):
                left_sc_d = np.arange(i,size_scaled_data+number_of_seasons-1,number_of_seasons)
                final_sc_d = sum_sc_d[left_sc_d]
                nul_data = np.where(final_sc_d == 0)[0] 
                data_diff_zero = final_sc_d
                data_diff_zero = data_diff_zero.astype(np.float) 
                data_diff_zero[data_diff_zero == 0] = 'nan'
                #data_diff_zero[nul_data] = []
                # the gamma distribution is not defined for x=0, and the probability of
                # zero participation q=(P(x=0) being positive we can therefore
                # calculate the cumulative probability see line 55
                q = len(nul_data) / len(final_sc_d)
                #    PARMHAT = gamfit(X) returns maximum likelihood estimates of the
                # parameters of a gamma distribution fit to the data in X.  PARMHAT(1)
                # and PARMHAT(2) are estimates of the shape and scale parameters A and B,
                # respectively.
                if not np.isfinite(data_diff_zero).all():
                    calc_alpha_beta_param1=np.nan
                    calc_alpha_beta_param2=np.nan 
                    Gam_fct =np.nan
                    SPI =np.full(len(left_sc_d), np.nan)
                else:
                    calc_alpha_beta_param = gamma.fit(data_diff_zero)
                        # calculating the cumulative probability H(x)=q+(1-q)(G(x)
                        # If m is the number of zeros in a precipitation time series,
                        # Thom(1966) states that q can be estimated by m/n. H(x) is transformed
                        # to the standard normal random variable Z with mean zero and variance
                        # 1, which is actually the SPI.
                    Gam_fct = q + (1 - q) * gamma.cdf(final_sc_d,calc_alpha_beta_param1,calc_alpha_beta_param2)
                        #P = gamcdf(X,A,B) returns the gamma cumulative distribution function
                        # with shape and scale parameters A and B, respectively, at the values in
                        # X.  The size of P is the common size of the input arguments.  A scalar
                        # input functions as a constant matrix of the same size as the other inputs.
                        #  norminv Inverse of the normal cumulative distribution function (cdf).
                        # X = norminv(P,MU,SIGMA) returns the inverse cdf for the normal
                        # distribution with mean MU and standard deviation SIGMA, evaluated at
                        # the values in P.  The size of X is the common size of the input
                        # arguments.  A scalar input functions as a constant matrix of the same
                        # size as the other inputs. Default values for MU and SIGMA are 0 and 1, respectively.
  
               
                    SPI[1:int(left_sc_d)] = stats.norm.ppf(Gam_fct)
       
        
            if len(SPI)< size_3rd1:
                add_v=size_3rd1-len(SPI)
                add_v=np.full(add_v, np.nan)
                SPI = np.append(SPI, add_v) 
            SPI_FINAL[n,m,:] = SPI
          
         
#SPI_G(prcp_3DArr,2,1) #example for running this code above.