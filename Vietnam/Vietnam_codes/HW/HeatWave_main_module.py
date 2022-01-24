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
lon_min = 105.665281
lon_max = 105.845963
lat_min =  9.954246
lat_max =  10.117987 
# filename='data.nc'
#      ncdisp(filename)
#     longitude=ncread(filename,'X')
#      latitude=ncread(filename,'Y')
#     time=ncread(filename,'T')
#     temperature=ncread(filename,'temp')
#         test=fix(time)
#     time_str = datetime(1960,1,1) + calmonths(test)  #convert the gregorian in days to date and time.
#    time1=time_str
#      time_str=datestr(time1)
#      res=[]
#  lonlatrect=[lon_min lon_max lat_min lat_max]
#      res.time=[]
#  res.time=Time
#   x=res.lon;y=res.lat
#   Lon1=lonlatrect(1); Lon2=lonlatrect(2)
#       inds=1:numel(x); inds=inds(:)
#    startx = ceil(interp1(x,inds,Lon1)) # x(startx)
#   endx   = ceil (interp1(x,inds,Lon2)) 
#  Lat1=lonlatrect(3); Lat2=lonlatrect(4)
#      inds=1:numel(y)
#   starty = floor(interp1(y,inds,Lat1))
#  endy   = floor (interp1(y,inds,Lat2))
#  countx=endx-startx; % x(startx+countx)
#      county=endy-starty
#data=data_CanTho    #this is for Iri data CHIRTS
#data=data_tmax_cpc    #this is for CPC data
#data_hist_rca4_final=data_hist_rca4_sim(29:end,:)    #RCA4 data goes from 1951 to 2021 and for the sake of comparison with CPC and Iri we took 1979--->2021
data=data_hist_rca4_final      #this is for CPC extrap data
consecutive_day_num=3
temperature=40
start_year=1979
end_year=2021
pdf_plusmines=10
startsummerday_s=day(datetime('01-Dec-1978'),'dayofyear') # start summer in Southern hemisphere the year should be modified based on the starting year.
endsummerday_s=day(datetime('28-Feb-1979'),'dayofyear') # end summer in Southern hemisphere
startsummerday=day(datetime('01-May-1979'),'dayofyear')  # start summer in Northern hemisphere
endsummerday=day(datetime('01-Sep-1979'),'dayofyear')  # end summer in Northern hemisphere
percentile_threshold=99
ehf_scale=0
method_used={'PDF_method','temperature_method'}   #PDF_method or temperature_method
switch method_used{1}
        case 'PDF_method'  
            threshold_data=pdf_threshold(data,pdf_plusmines,percentile_threshold)
            [heatwave_data,length_heatwave_data,binary_result]=calc_pdf_heatwave_event(data,threshold_data,consecutive_day_num,[],[],start_year,end_year)

        case 'temperature_method'
            [heatwave_data,length_heatwave_data,binary_result]=calc_temperature_heatwave(data,[],consecutive_day_num,temperature,start_year,end_year)
end


# calculate first day, last day, longest and ... of heatwave
[First_HW_DOY,Last_HW_DOY,Length_Longest_HW,HW_Magnitude_HWM,HW_Amplitude_HWA]=create_summary(binary_result,data,consecutive_day_num)

# plot HW duration
if  ~isempty(length_heatwave_data):
    save_fig=handles.chk_eachfig
    plot_heatwave_duration(length_heatwave_data,start_year,end_year,save_fig,target_coordinate{1},target_coordinate{2})
    # for example use this one :
    # plot_heatwave_duration(length_heatwave_data,start_year,end_year,0,thelon_iri_f,thelat_iri_f);
end

### $$$$$$$$$$$$$$$$$$$$$$$$   calc_pdf_heatwave_event   $$$$$$$$$$
def [output,length_heatwave_data,binary_result]=calc_pdf_heatwave_event(data,threshold_data,consecutive_day_num,start_summer,end_summer,start_year,end_year)
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
start_y=find(ismember(data(:,1),num2str(start_year))>0)
end_y=find(ismember(data(:,1),num2str(end_year))>0)
#
heatwave_data{size(data,1),1}={}
heatwave_data(:)={'0'}
length_heatwave_data{size(data,1),1}={}
length_heatwave_data(:)={'0'}
#
binary_result={}
for year in range(start_y, end_y):
    heatwave_data{year,1}=data{year,1}
    length_heatwave_data{year,1}=data{year,1}
    convert_data=reshape(data{year,2},[],size(data{year,2},3))
    #
    binary_result{year,1}=data{year,1}
    binary_result{year,2}=transpose(zeros(size(convert_data)))
    for coordinate in range (1, size(convert_data,1)):
        if size(convert_data,2)< size(threshold_data,1):
            new_th=size(convert_data,2)
            threshold_data=threshold_data(1:new_th,:)
        
        thresh=threshold_data(:,coordinate)'
        
        dd=convert_data(coordinate,:)
        #PDF method base on summer data (Extract just summer threshold/temperature day data)
        if ~isempty(start_summer) && ~isempty(end_summer):
            thresh=thresh(start_summer:end_summer)
            dd=dd(start_summer:end_summer)
        
        # leap year
        if size(dd,2)==366:
            dd=[dd(1,1:59),dd(61:end)]
        
        
        if length(find(isnan(dd)))>65:   # more than 65 missed data, then do not process
            heatwave_data{year,coordinate+1}=-1
            length_heatwave_data{year,coordinate+1}=-1
            #
            nan_item=find(isnan(dd'))
            binary_result{year,2}(nan_item,coordinate)=np.nan
        else
            #  algorithm in order to find event (find event days bigger-equal consecutive day)
            matrix_data=zeros(size(dd'))
            matrix_data(dd'>thresh')=1
            
            datazero=[0;find(matrix_data==0 | isnan(matrix_data));length(matrix_data)+1]
            datadiffzero=diff(datazero)
            datafinddifzero=find(datadiffzero>consecutive_day_num)
            # heatwave event
            heatwave_data{year,coordinate+1}=datafinddifzero    # heatwave event number
            # duration heatwave
            length_heatwave_data{year,coordinate+1}=datadiffzero(find(datadiffzero>consecutive_day_num))-1   ### total heatwave (durations)
            for ii in range(1, size(datafinddifzero,1)):
                index_1=datazero(datafinddifzero(ii),1)
                #index_2=datazero(datafinddifzero(ii)+1,1)
                days_duration=datadiffzero(datafinddifzero(ii),1)
                binary_result{year,2}(index_1+1:index_1+days_duration-1,coordinate)=int8(1)
            
            nan_item=find(isnan(dd'))
            binary_result{year,2}(nan_item,coordinate)=np.nan
        
    
    

return output=heatwave_data


### $$$$$$$$$$$$$$$$$$$$$$$$$$$   calc_temperature_heatwave  $$$$$$
def [output,length_heatwave_data,binary_result]=calc_temperature_heatwave(data,all_summer_data,consecutive_day_num,temperature,start_year,end_year)
#################
#HW_Record_Constant_Threshold_TMAX_35_ConsDays_4_2014 last days have problem
#HW_Record_Constant_Threshold_TMAX_35_ConsDays_4_2015 first days
#################
#purpose : calculate Heatwave event/duration base on temperature/summer method

#Input :
# data : a 3D matrix-temperature data
# all_summer_data : summer data threshold (for summer method)
# consecutive_day_num : consecusive days
# temperature : temperature threshold (for temperature method)
# start_year : start year
# end_year : end year

# find index of start/end year
start_y=find(ismember(data(:,1),num2str(start_year))>0)
end_y=find(ismember(data(:,1),num2str(end_year))>0)

#initialize
heatwave_data{size(data,1),1}={}
heatwave_data(:)={'0'}
length_heatwave_data{size(data,1),1}={}
length_heatwave_data(:)={'0'}
#
binary_result={}
for year in range(start_y, end_y):
    heatwave_data{year,1}=data{year,1}
    length_heatwave_data{year,1}=data{year,1}
    convert_data=reshape(data{year,2},[],size(data{year,2},3))
    #
    binary_result{year,1}=data{year,1}
    binary_result{year,2}=transpose(zeros(size(convert_data)))
    for coordinate in range (1, size(convert_data,1)):
        if isempty(temperature):
            threshold=all_summer_data(coordinate,1)#*scale
        else:
            threshold=temperature
        
        dd=convert_data(coordinate,:)
        
        if length(find(isnan(dd)))>65:    # more than 65 missed data, ignore
            heatwave_data{year,coordinate+1}=-1
            length_heatwave_data{year,coordinate+1}=-1
            #
            nan_item=find(isnan(dd'))
            binary_result{year,2}(nan_item,coordinate)=np.nan
        else
            # algorithm in order to find event (find event days bigger-equal consecutive day)
            matrix_data=zeros(size(dd'))
            matrix_data(dd>threshold)=1
            
            datazero=[0;find(matrix_data==0 | isnan(matrix_data));length(matrix_data)+1]
            datadiffzero=diff(datazero)
            datafinddifzero=find(datadiffzero>consecutive_day_num)
            # heatwave event
            heatwave_data{year,coordinate+1}=datafinddifzero
            # duration heatwave
            length_heatwave_data{year,coordinate+1}=datadiffzero(find(datadiffzero>consecutive_day_num))-1
            for ii in range(1, size(datafinddifzero,1)):
                index_1=datazero(datafinddifzero(ii),1)
                days_duration=datadiffzero(datafinddifzero(ii),1)
                binary_result{year,2}(index_1+1:index_1+days_duration-1,coordinate)=int8(1)
            
            nan_item=find(isnan(dd'))
            binary_result{year,2}(nan_item,coordinate)=np.nan
            
        
    


return output=heatwave_data


### $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  plot_heatwave_duration  $$$$$$$$$$$$$$$$$
def plot_heatwave_duration(length_heatwave_data,start_year,end_year,save_fig,lon_con,lat_con)

# purpose : plot duration Heatwave data

#Input :
# length_heatwave_data : Heatwave duration
# start_year :  start year
# end_year : end year
# saveastxt : save Heatwave Event data as txt file

# load target country mask file
load('./result/new_mask_map')
mask_map=new_mask_map
start_y=find(ismember(length_heatwave_data(:,1),num2str(start_year))>0)
end_y=find(ismember(length_heatwave_data(:,1),num2str(end_year))>0)
###
#I=edge(mask_map)
# checked save txt checkbok checked
# if saveastxt==1
#     fid=fopen('./result/Heatwave_duration.txt','w');
# end

matrix=[]
# matrix_copy is a copy of matrix that mask file is not apply on it
matrix_copy=[]
###
h = figure('name','Duration')
set(gcf,'color','w','units','normalized','position',[0.05 0.05 0.75 0.85],'paperpositionmode','auto')
###
for year in range(start_y, end_y):
    
    for i in range(2, size(length_heatwave_data,2)):
        if length_heatwave_data{year,i}==-1:
            matrix(year,i-1)=nan;%-1
        else:
            matrix(year,i-1)=sum(length_heatwave_data{year,i})
        
    
    
    matrix_copy(year,:)=matrix(year,:)
    buni=reshape(mask_map,1,[])
    #apply mask file on matrix data
    matrix(year,find(buni==0))=nan;%0;%min(min(data))


n = max(max(matrix))
if ~isempty(find(matrix==-1)):
    heatwavecolormap=[[0,0,0;1,1,1];[ones(n-1,1) linspace(1,0,n-1)' zeros(n-1,1)]];%cmap]
else:
    heatwavecolormap=[[1,1,1];[ones(n-1,1) linspace(1,0,n-1)' zeros(n-1,1)]];%cmap]

m=0
for year in range(start_y, end_y):
    m=m+1
    dd=matrix(year,:)
    data=reshape(dd,size(mask_map,1),size(mask_map,2))
    ##
    if m==1:
        Position=[0.1,0.75,0.2,0.2]
    else:
        pos=get(fig(m-1),'position')
        newpos=[pos(1)+pos(3)+0.1,pos(2),pos(3),pos(4)]
        if newpos(1)>0.95:
            newpos=[0.1, pos(2)-pos(4)-0.1,pos(3), pos(4) ]
        
        Position=newpos
    
    #
    fig(m)=scrollsubplot(m,Position)
    ###
    data2=transpose(data)
    img_=imagesc(flipud(data2))
    set(img_,'Xdata',[min(lon_con) max(lon_con)])
    xlim([min(lon_con) max(lon_con)])
    set(img_,'ydata',[min(lat_con) max(lat_con)])
    ylim([min(lat_con) max(lat_con)])
    set (gca,'YDir','normal')
    colormap(fig(m),heatwavecolormap)
    hold on
    plot(lon_con,lat_con,'LineWidth',2)
    title(strcat('# Heatwave days', {' '} , num2str(length_heatwave_data{year,1})))
    xlabel('Longitude')
    ylabel('Latitude')
    
    if save_fig==1:
        filename=sprintf('./result/figures/fig_%s_%s.jpg','days',num2str(length_heatwave_data{year,1}))
        title_name=strcat('# Heatwave days', {' '} , num2str(length_heatwave_data{year,1}))
        save_each_fig(data2,filename,title_name,lon_con,lat_con,heatwavecolormap,min(min(matrix)),n)
    
    
    colormap(fig(m),heatwavecolormap)
%     if min_value==max_value:
%         max_value=max_value+0.01*max_value
%         min_value=min_value-0.01*min_value
%     
%     caxis([min(min(matrix_copy)) n])
    min_non_zero=min(min(matrix_copy(matrix_copy~=0)))
    if abs(min_non_zero-0)>5:
        if abs(floor(min_non_zero)-min_non_zero)<0.5:
            caxis([min_non_zero-1 n])
        else:
            caxis([min_non_zero n])
        
    else:
        caxis([min(0,min(min(matrix_copy))) n])
    
    pause(0.2)

colorbar('Position', [0.92  0.2  0.02  0.7])


##### $$$$$$$$$$$$$$$$$$$$$$    pdf_threshold   $$$$$$$$$$$$$$$$$$$$$$$$$
def threshold=pdf_threshold(data,txt_plusminusdays_num,threshold_percental)
# purpose : calculate PDF threshold

# Input :
# data : a 3D matrix-temperature data
# txt_plusminusdays_num : +- number days for calculating PDF threshold
# threshold_percental : threshold percental

# Refrence:
# Stefanon, M., D’Andrea, F., & Drobinski, P. (2012). Heatwave classification over 
#      Europe and the Mediterranean region. Environmental Research Letters, 7(1), 014023.

h_waiter = waitbar(0,'Please wait...','Name','Calculate pdf')

data_all_temp=[]

#arrange temperature data
for year in range(1, size(data,1)):
    dd=reshape(data{year,2},[],size(data{year,2},3))
    ddd=transpose(dd)
    data_all_temp=[data_all_temp;[str2num(data{year,1})*ones([size(ddd,1),1]),(1:size(ddd,1))',ddd]]


threshold=[]
if data_all_temp(end,2)<365:
    except_year=1
else:
    except_year=0

# for each day of year, calculate +-days of target day temperature
for day in range(1, 365)
    matrix=[]
    for year in range(min(data_all_temp(:,1)), max(data_all_temp(:,1))- except_year):
        index=find(data_all_temp(:,1)==year & data_all_temp(:,2)==day)
        days_txt_plusminus=[index-txt_plusminusdays_num:index+txt_plusminusdays_num]
        #reset wrong data
        days_txt_plusminus(days_txt_plusminus<1)=1
        days_txt_plusminus(days_txt_plusminus>size(data_all_temp,1))=size(data_all_temp,1)
        ###
        dd=data_all_temp(unique(days_txt_plusminus),3:end)
        matrix=[matrix;dd]
    
    threshold(end+1,:)=prctile(matrix,threshold_percental)
    waitbar(day/365)

## save threshold threshold
delete(h_waiter)


#### $$$$$$$$$$$$$$$$$$$$$$$$   scrollbar   $$$$$$$$$$$$$$$$$$
def ax =scrollsubplot(thisPlot,position):
ax = axes('units','normal','Position', position)
set(ax,'units',get(gcf,'defaultaxesunits'))

scroll_ = findall(gcf,'Type','uicontrol','Tag','scrollbar')

if isempty(scroll_):
    uicontrol('Units','normalized',...
        'Style','Slider',...
        'Position',[.98,0,.02,1],...
        'Min',0,...
        'Max',1,...
        'Value',1,...
        'visible','off',...
        'Tag','scrollbar',...
        'Callback',@(scr,event) scroll(1))

#
if ( 9 < thisPlot || thisPlot < 1 ):
    set(scroll_,'visible','on')

scroll(1)
set(scroll_,'value',1)


def scroll(vauel):
ui_hndl_callback = findall(gcf,'Type','uicontrol','Tag','scrollbar')
axis_ = findall(gcf,'Type','axes')

for ii in range(length(axis_):-1:1):
    a_pos(ii,:) = get(axis_(ii),'position')


pos_y_range = [min(.07,min(a_pos(:,2))) max(a_pos(:,2) + a_pos(:,4) )+.07-.9]

val = get(ui_hndl_callback,'value')
step = ( vauel - val) * diff(pos_y_range)


for ii in range(1, length(axis_)):
    set(axis_(ii),'position',get(axis_(ii),'position') + [0 step 0 0])


set(ui_hndl_callback,'callback',@(scr,event) scroll(val))
