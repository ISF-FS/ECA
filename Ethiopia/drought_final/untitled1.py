# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 12:20:11 2022

@author: daou
"""

# Create an N x N magic square. N must be odd.
import numpy as np
# def magic_square(n):
   
#     if n % 4 != 0:
#         raise ValueError('n must be a multiple of 4')
#     M = np.empty([n, n], dtype=int)
#     M[:, :n//2] = np.arange(1, n**2//2+1).reshape(-1, n).T
#     M[:, n//2:] = np.flipud(M[:, :n//2]) + (n**2//2)
#     M[1:n//2:2, :] = np.fliplr(M[1:n//2:2, :])
#     M[n//2::2, :] = np.fliplr(M[n//2::2, :])
#     return M
# X=magic_square(4)
# print(X)

# latit = np.reshape(X, -1, order='F')
# print(latit)

# lontit = np.reshape(X, (np.product(X.shape,))
# print(lontit)

lat = np.array([26.933899, 26.957203, 26.783846, 26.645524, 26.897796, 26.925359, \
        26.914768, 26.853491, 26.845099, 26.82651 , 26.842772, 26.825905, \
        26.80465 , 26.788649, 26.704277, 26.71005 , 26.755412, 26.678449, \
        26.725649, 26.720599, 26.71255 , 26.6649  , 26.664699, 26.663149, \
        26.66875 , 26.638517, 26.59309 , 26.617449, 26.620079, 26.596795, \
        26.577049, 26.524585, 26.524158, 26.523737, 26.520284, 26.547349, \
        26.463399, 26.45905 , 26.45558 , 26.453699, 26.449999, 26.397299, \
        26.4084  , 26.40875 , 26.379113, 26.3809  , 26.349068, 26.346349, \
        26.348015, 26.347957])

lon = np.array([-80.128799, -80.098284, -80.748947, -80.550704, -80.596929, \
        -80.220966, -80.07466 , -80.190281, -80.083904, -80.213493, \
        -80.0591  , -80.630096, -80.075301, -80.069885, -80.656841, \
        -80.190085, -80.08955 , -80.041179, -80.1324  , -80.091746, \
        -80.068579, -80.090698, -80.1254  , -80.151401, -80.058749, \
        -80.283371, -80.206901, -80.090649, -80.055001, -80.128711, \
        -80.076435, -80.080105, -80.06398 , -80.178973, -80.110519, \
        -80.057701, -80.064251, -80.07875 , -80.139247, -80.104316, \
        -80.188545, -80.21902 , -80.092391, -80.1575  , -80.102028, \
        -80.16885 , -80.116401, -80.08385 , -80.241305, -80.158855])
    
lat_min=3.233833
lat_max=11.0833
lon_min=39.0833
lon_max=47.9667    
# create meshgrid
[X, Y ] = np.meshgrid(np.linspace(lon_min,lon_max,len(lon)), np.linspace(lat_min,lat_max,len(lat)))
print(np.shape(X), np.shape(Y))
print(X)
string='Somali'
result = ""
for i in range(1,100):
    j=str(i)
    name=string.join(j)
    result += name
print(result)    
#from itertools import product

#string = input("string: ")
# string='Somali%d%d'
# parts = string.split("%d")
# num_digits = len(parts) - 1
# if num_digits > 0:
#     for digits in product("0123456789", repeat=num_digits):
#         print(
#             "".join(
#                 part + digit for part, digit in zip(parts, digits)
#             ) + parts[-1]
#         )
from itertools import product
def ev_name(string):
    #string = input("string: ")
    f_name=[]
    counter=0
    num_digits = string.count("%d")    #Example: 'Somali%d%d' or 'HND%d'
    if num_digits > 0:
      digit_str = string.replace("%d", "{}")
      #print(digit_str)
      for digits in product("0123456789", repeat=num_digits):
            print(digit_str.format(*digits))   
            ev_name=digit_str.format(*digits)
            print(ev_name)
            print(type(ev_name))
            #out = f_name+[ev_name]
            out1=[ev_name]
            #print(out)
            print(out1)
            # out = ['+'.join(out)]
            # print(out)
            if counter==0:
                out=[f_name, ev_name]
                print(out, 'am euqal zero')
                #f_name=out[-1]
            elif counter==-1:
                f_name=out[-1]
                out = [f_name, ev_name]
                print(out, 'am euqal one')
            else:
                #f_name=out[-1+counter:]
                #f_name=[ev_name]
                f_name= out+out1
                out=f_name
            print(f_name)  
            counter=counter-1
    return f_name
ev_name('HND%d')   
#tdate = [721166, 734447, 734447, 734447, 721167, 721166, 721167, 721200, 721166, 721166]
tdate=[2020]
test=np.repeat(tdate, repeats = [100], axis=0)
print(test)
# test=pd.to_datetime(tdate)
# test1= datetime.datetime.fromtimestamp(721166)
# print(test1)
# print(test)

#s = ' ',
#f_name=s.join(list(ev_name))  
#print(f_name) 

# r = ['{}{}'.format(ch, x) for x in range(11) for ch in 'Somali']
# print(r)
# # ['X0', 'Y0', 'Z0', 'X1', 'Y1', 'Z1']
