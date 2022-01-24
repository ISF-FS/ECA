# -*- coding: utf-8 -*-
"""
%This code calculate the returning periods of extreme precipitation from RCA4 CAM44 for
%2,5,10,15,25,35,50,75,100
% David Daou 2020 14 February, Saint Valentine's Day
% This code first imports the data, then try to fit a model to the data
% Then we calculate the returning periods and finally we check the
% confidence interval for each returning year or period.
%% Input parameters
% data is a matrix (2D or 3D array) of precipitation data
% daily_time is a vector (1D Array, that can be numeric or cell or string)
% of the date and time
%start_year and end_year are the starting and ending year of the precipitation object
%of study  respectively.

@author: daou
"""

import numpy as np

def return_periods (data, daily_time, start_year, end_year, lat ,lon)   
#convert the data to mm/day
orig_data=data   #(keep a copy of the data in original untis which is for RCA4 kg.m-2.s-1)
#data=data*24*60*60
#daily_data_time  = start_year+1/366:1/366:end_year


#We have monthly data and we need annual maxima data for both variables.
#monthV=start_year+1/12:1/12:end_year;
yearV   = start_year:1:end_year



# 2- now we calculate the Returning periods
# We want to know the return levels of the following return periods: 2, 10, 25, 50, 100 using a GEV distribution. 
# First, we need to calculate the distribution parameters.
ret_y = [10;25;50;75;100]
# ret_y=1:1:30
# ret_y=ret_y'
returning_period_mat=zeros(numel(data(:,1,1)),numel(data(1,:,1)),numel(ret_y))
%# We enter the return periods (in years) and calculate the equivalent probabilities.
#ret_y = [2;5;10;15;20;25;35;50;75;100]
ret_Per = 1-1./ret_y
for i in range (1,len(lon)):
    for  j in range(1, len(lat)):
    
       pcp=squeeze(data(i, j,:))
       prcp=pcp(~isnan(pcp))
       if isempty(prcp):
           for k in range(1, len(ret_y)):
               returning_period_mat(i,j,k)=np.nan
           
       else
# Distribution fitting
#Now, we want to fit the GEV distribution for Extreme Events Analysis.
#There is a Matlab function to get the parameters of the distribution. parmhat = gevfit(X) returns maximum likelihood estimates of the parameters
#for the generalized extreme value (GEV) distribution given the data in X. 
%#parmhat(1) is the shape parameter, k, parmhat(2) is the scale parameter, sigma, and parmhat(3) is the location parameter, mu.
            #parm_Prcp    = gevfit(prcp);
            parm_Prcp    = gamfit(prcp);

            #  Return levels
            # Now we can calculate the return levels associated with each return periods.
            # X = gevinv(P,k,sigma,mu) returns the inverse cdf of the generalized extreme value (GEV) distribution with shape parameter k, scale parameter sigma, and location parameter mu, evaluated at the values in P. 
            # The size of X is the common size of the input arguments. A scalar input functions as a constant matrix of the same size as the other inputs.
            #  Default values for k, sigma, and mu are 0, 1, and 0, respectively.
            # When k < 0, the GEV is the type III extreme value distribution. When k > 0, the GEV distribution is the type II, or Frechet, extreme value distribution. 
            # If w has a Weibull distribution as computed by the wblinv function, then -w has a type III extreme value distribution and 1/w has a type II extreme value distribution. 
            # In the limit as k approaches 0, the GEV is the mirror image of the type I extreme value distribution as computed by the evinv function.
            # The mean of the GEV distribution is not finite when k ? 1, and the variance is not finite when k ? 1/2. The GEV distribution has positive density only for values of X such that k*(X-mu)/sigma > -1.
            # w1 = gevinv(ret_Per,parm_Prcp(1),parm_Prcp(2),parm_Prcp(3)); %Generalized extreme value inverse cumulative distribution function
             w1 = gaminv(ret_Per,parm_Prcp(1),parm_Prcp(2))   # Generalized Gamma value inverse cumulative distribution function
            for k in range(1, len(w1))
                returning_period_mat(i,j,k)=w1(k)
            
       
    

return returning_period_mat