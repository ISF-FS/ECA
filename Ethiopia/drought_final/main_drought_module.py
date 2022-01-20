# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 20:56:21 2022

@author: daou
"""
# this is the first test version of the drought module called v0.0.1
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
import PySimpleGUI as sg
from DRT_SPI import  *
from read_chirps import *
event, values = sg.Window('Choose an option', [[sg.Text('Select an index amongst these choices, if none is selected it will be aborted->'), sg.Listbox(['a-  SPI_P (Standard Precipitation Index using a polynomial function)', 'b-  SPI_G:(Standard Precipitation Index using gamma distribution)', 'c-  SPEI_P (Standard Precipitation & Evapotranspiration Index using Pearson)', 'd-  SPEI_G (Standard Precipitation & Evapotranspiration Index using Gamma distribution)', 'e-  MSDI (Multivariate Standardized Drought Index)', 'f-   PDSI (Palmer Drought Severity Index)','g-  Z_index (Palmer Z index)'], size=(100, 7), key='LB')],
    [sg.Button('Ok'), sg.Button('Cancel')]]).read(close=True)

if event == 'Ok':
    sg.popup(f'You chose {values["LB"][0]}')
    if (values["LB"][0])=="a-  SPI_P (Standard Precipitation Index using a polynomial function)":
        bbb=values["LB"][0]
        print(bbb)
        input_data=read_cut_CHIRPS_data(8.8333,14.533,39.65,42.4) # values taken here are for Afar-Ethiopia
        print(input_data)
        #tre_etoile(5)
    elif (values["LB"][0])=="b-  SPI_G:(Standard Precipitation Index using gamma distribution)":
        ccc=values["LB"][0]
        print(ccc)
        input_data=read_cut_CHIRPS_data(8.8333,14.533,39.65,42.4) # values taken here are for Afar-Ethiopia
        print(input_data)
        SPI_G(input_data,2,1) #example for running this code above.
    elif (values["LB"][0])=="c-  SPEI_P (Standard Precipitation & Evapotranspiration Index using Pearson)":
        ddd=values["LB"][0]
        print(ddd)
    elif (values["LB"][0])=="d-  SPEI_G (Standard Precipitation & Evapotranspiration Index using Gamma distribution)":
        eee=values["LB"][0]
        print(eee)
    elif (values["LB"][0])=="e-  MSDI (Multivariate Standardized Drought Index)":
        fff=values["LB"][0]
        print(fff)
    elif (values["LB"][0])=="f-   PDSI (Palmer Drought Severity Index)":
        ggg=values["LB"][0]
        print(ggg) 
    elif (values["LB"][0])=="g-  Z_index (Palmer Z index)":
        hhh=values["LB"][0]
        print(hhh)        
else:
    sg.popup_cancel('User aborted') # if user closes window or clicks cancel
    #break