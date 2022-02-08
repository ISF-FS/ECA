# -*- coding: utf-8 -*-
"""
Created in August 2021
This code calculates the WSDI (Warm Spell Duration Index) for Heatwaves(HW)
This code works properly with only daily data using Temperature, it can be Tmax, Tmean or Tmin
Depending on the choice one will have to tweak some constant parameters, 
however it is recommended to use Tmax or Tmean.
@author: daou
"""
import numpy as np
from scipy.io import loadmat
datamat = loadmat('dataforpython.mat')
data_CanTho=datamat.get("dataforpython")
lon_min = 105.665281
lon_max = 105.845963
lat_min =  9.954246
lat_max =  10.117987 


data=data_CanTho    #this is for Iri data CHIRTS
#data=data_tmax_cpc    #this is for CPC data
#data_hist_rca4_final=data_hist_rca4_sim(29:end,:)    #RCA4 data goes from 1951 to 2021 and for the sake of comparison with CPC and Iri we took 1979--->2021
#my_date = datetime.date(1978,12,1)   # time = 00:00:00
#startsummerday_s=my_date.toordinal() 
dtss = datetime.datetime.strptime('1982.12.01', '%Y.%m.%d')
ttss = dtss.timetuple()
dtes = datetime.datetime.strptime('1983.02.28', '%Y.%m.%d')
ttes = dtes.timetuple()
dtss_ne = datetime.datetime.strptime('1983.05.01', '%Y.%m.%d')
ttss_ne = dtss_ne.timetuple()
dtes_ne = datetime.datetime.strptime('1983.09.01', '%Y.%m.%d')
ttes_ne = dtes_ne.timetuple()
startsummerday_s=ttss.tm_yday # start summer in Southern hemisphere the year should be modified based on the starting year.
endsummerday_s=ttes.tm_yday # end summer in Southern hemisphere
startsummerday=ttss_ne.tm_yday  # start summer in Northern hemisphere
endsummerday=ttes_ne.tm_yday  # end summer in Northern hemisphere

consecutive_day_num=3 # consecutive days considered as heatwave
temperature=40   #temperature threshold for percentiles and declaration of heatwave event, here
                 # one needs to be careful in the selection, depending if using Tmax or Tmean
start_year=1983  # based on the data selected (verify which year the data start)
end_year=2016    # based on the data selected (verify which year the data end)
pdf_val=10 #+- number of days for calculating PDF threshold
percentile_threshold=95  # this number can be modified depending on the region
ehf_scale=0
def ismember(A, B):
    return [ np.sum(a == B) for a in A ]

##### $$$$$$$$$$$$$$$$$$$$$$    pdf_threshold   $$$$$$$$$$$$$$$$$$$$$$$$$
def pdf_threshold(data,txt_plusminusdays_num,threshold_percental):
# purpose : calculate PDF threshold

# Input :
# data : a 3D matrix-temperature data
# txt_plusminusdays_num : +- number days for calculating PDF threshold
# threshold_percental : threshold percental

# Refrence:
# Stefanon, M., D’Andrea, F., & Drobinski, P. (2012). Heatwave classification over 
#      Europe and the Mediterranean region. Environmental Research Letters, 7(1), 014023.

#h_waiter = waitbar(0,'Please wait...','Name','Calculate pdf')
    from tqdm import tdqm
    
    LENGTH = 365 # Number of iterations required to fill pbar
    
    pbar = tqdm(total=LENGTH) # Init pbar
    
    data_all_temp=np.array([])
    #arrange temperature data
    for year in range(0, data[:,0].size):
        test=data[year,1]
        nb_elt=test[year,0,:].size
        dd=test.transpose(1,0,2).reshape(-1,nb_elt)
        ddd=np.transpose(dd)
        create_arr=int(data[year,0])*np.ones((ddd[:,0].size,1))
        arr_enum=np.transpose(np.arange(ddd[:,0].size))
        con_arr=np.column_stack((create_arr,arr_enum,ddd))
        if (year==0):
            data_all_temp=con_arr
        else:
            data_all_temp=np.vstack(data_all_temp,con_arr)
    
    
    threshold=np.zeros((nb_elt*data[:,0].size,test[0,:,0].size*test[:,0,0].size))
    if data_all_temp[-1,1]<364:
        except_year=1
    else:
        except_year=0
    
    # for each day of year, calculate +-days of target day temperature
    for day in range(0, 364):
        matrix=np.array([])
        for year in range(min(data_all_temp[:,0]), max(data_all_temp[:,0])- except_year):
            index=len(np.intersect1d((data_all_temp[:,0]==year), (data_all_temp[:,1]==day)))
            days_txt_plusminus=np.arange(index-txt_plusminusdays_num, index+txt_plusminusdays_num)
            #reset wrong data
            days_txt_plusminus[days_txt_plusminus<0]=0
            days_txt_plusminus[days_txt_plusminus>data_all_temp[:,0].size]=data_all_temp[:,0].size
            ###
            dd=data_all_temp[np.unique(days_txt_plusminus),2:]
            if (year==min(data_all_temp[:,0])):
                matrix=dd
            else:
                matrix=np.vstack(matrix,dd)
        
        threshold[day,:]=np.percentile(matrix, threshold_percental, interpolation='midpoint')
        #waitbar(day/364)
        pbar.update(n=1) # Increments counter
        
    
        
    ## save threshold threshold
    pbar.hide()
    
    return threshold


### $$$$$$$$$$$$$$$$$$$$$$$$   calc_pdf_heatwave_event   $$$$$$$$$$
def calc_pdf_heatwave_event(data,threshold_data,consecutive_day_num,start_summer,end_summer,start_year,end_year):
#purpose : calculate Heatwave event/duration base on PDF method
#error
#Input :
# data : a 3D matrix-temperature data
# threshold_data : PDF threshold
# consecutive_day_num : consecusive days
# start_year : start year
# end_year : end year
# start_summer :start summer day (for PDF method base on summer data)
# end_summer : end summer day (for PDF method base on summer data)

# Refrence:
# Stefanon, M., D’Andrea, F., & Drobinski, P. (2012). Heatwave classification over
#       Europe and the Mediterranean region. Environmental Research Letters, 7(1), 014023.

# find index of start/end year
    #start_y=find(ismember(data(:,1),num2str(start_year))>0)
    end_y=np.where(np.in1d(data[:,0], str(end_year)))[0]
    start_y=np.where(np.in1d(data[:,0], str(start_year)))[0]
    #
    a = np.zeros(data[:,0].size)
    b = a.astype(str)
    hw_data=np.array([[b, a]])
    heatwave_data = np.empty(hw_data.shape, dtype=object)
    
    length_heatwave_data=heatwave_data
    #
    binary_result={}
    for year in range(start_y, end_y):
        heatwave_data[year,0]=data[year,0]
        length_heatwave_data[year,0]=data[year,0]
        test=data[year,1]
        nb_elt=test[year,0,:].size
        convert_data=test.transpose(1,0,2).reshape(-1,nb_elt)
        #convert_data=np.transpose(dd)
        #
        cell_arr = np.array([[data[year,0], data[year,1]]])
        binary_result = np.empty(cell_arr.shape, dtype=object)
        binary_result[year,0]=data[year,0]
        binary_result[year,1]=np.transpose(np.zeros(convert_data.shape))
        for coordinate in range (0, convert_data[:,0].size):
            if (convert_data[0,:].size< threshold_data[:,0].size):
                new_th=convert_data[0,:].size
                threshold_data=threshold_data[0:new_th,:]
            
            thresh=np.transpose(threshold_data[:,coordinate])
            
            dd=convert_data[coordinate,:]
            #PDF method base on summer data (Extract just summer threshold/temperature day data)
            if  np.all(start_summer==0) & np.all(end_summer==0):
                thresh=thresh[start_summer:end_summer]
                dd=dd[start_summer:end_summer]
            
            # leap year
            if  dd.size==366:
                dd=np.concatenate([dd[0:58],dd[59:]])
            
            
            if  np.count_nonzero(np.isnan(dd))>65:   # more than 65 missed data, then do not process
                heatwave_data[year,coordinate+1]=-1
                length_heatwave_data[year,coordinate+1]=-1
                #
                nan_item=np.isnan(dd)
                binary_result[year,1](nan_item,coordinate)=np.nan
            else:
                #  algorithm in order to find event (find event days bigger-equal consecutive day)
                matrix_data=np.zeros(dd.size)
                mat_gr= np.greater(dd,thresh)
                matrix_data=mat_gr.astype(int)
                matrix_data[np.isnan(matrix_data)]=0
                idx_zero=np.argwhere(matrix_data==0)
                len_arr=len(matrix_data+1)
                idx_zero=np.append(idx_zero,len_arr)
                datazero==np.append(0,idx_zero)
                datadiffzero=np.diff(datazero)
                datafinddifzero=np.where(datadiffzero> consecutive_day_num)
                # heatwave event
                heatwave_data[year,coordinate+1]=datafinddifzero    # heatwave event number
                # duration heatwave
                length_heatwave_data[year,coordinate+1]=datadiffzero[datafinddifzero]-1   ### total heatwave (durations)
                for ii in range(1, len(datafinddifzero)):
                    index_1=datazero[datafinddifzero[ii]]
                    #index_2=datazero(datafinddifzero(ii)+1,1)
                    days_duration=datadiffzero[datafinddifzero[ii]]
                    right_idx=index_1+days_duration-1
                    left_idx=index_1+1
                    binary_result[year,1][int(left_idx):int(right_idx),coordinate]=int(1)
                nan_item=np.isnan(dd)
                binary_result[year,1][nan_item,coordinate]=np.nan
            
        
        

return heatwave_data, length_heatwave_data, binary_result


threshold_data=pdf_threshold(data,pdf_val,percentile_threshold)
heatwave_data, length_heatwave_data, binary_result=calc_pdf_heatwave_event(data,threshold_data,consecutive_day_num,[],[],start_year,end_year)

# calculate first day, last day, longest and ... of heatwave
#[First_HW_DOY,Last_HW_DOY,Length_Longest_HW,HW_Magnitude_HWM,HW_Amplitude_HWA]=create_summary(binary_result,data,consecutive_day_num)

