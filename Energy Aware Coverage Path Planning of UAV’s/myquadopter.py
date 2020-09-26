# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 00:58:59 2019

@author: farhan
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from sympy import *



alpha_in_degree = 122.6/2  # angle of view
alpha = math.radians(alpha_in_degree)
I_x = 4000
I_y = 3000
ro = I_x/I_y  # I_x/I_y or aspect ratio  of go pro camera 12mp
desired_spatial_resolution = 72.5555    #pixel/meter

h_max = I_x/(2*desired_spatial_resolution*math.tan(alpha))
print("Max height that can be obtained for desired resolution", h_max)


L_x = 2*h_max*math.tan(alpha)
L_y = L_x/ro
area = L_x*L_y

print("X of area in meters",L_x)
print("Y of area in meters",L_y)
area = L_x*L_y
print("Area captured in meter square", area)


#Energy Model
# Energ consumed while accelerating at max accelaration
# given a velocity we will compute the time it will to reach it and then
# calculate from chart below the value of power consumed in that time.
#print("Below is velocity time model with with max accelaration ")
v_intial = 0     # user given velocity and accelration 
v_final  = 4
acc = 0.8
t = (v_final - v_intial)/acc
#print("time calculated by given velocity of user",t)
def v_acc(v_in):
#velocity-accelration profile with time
    v_t =[0,5,10,15,20,25,30]
    v_y =[0,4,8.5,12,13,14,15]

    z = np.polyfit(v_t, v_y, 5)
    f = np.poly1d(z)
    #print(z)
    #print(f(5))

# calculate new x's and y's
    x_new = np.linspace(v_t[0], v_t[-1], 50)
    y_new = f(x_new)


    #plt.plot(v_t,v_y,'o', x_new, y_new)
    #plt.axis([0,35,0,20])
    #plt.show()

#find time value from given velocity value
    hj = v_in-f
    kl = hj.c
    jk =np.roots(kl)
    for v in jk:
        if v <= 0 or v >= 35:
            v = jk
        else:
            v_o = v


   #integratrion for distance
    n=f.integ()
    nj = n(v_o)-n(0)
    #print("power conumed in t time accelration ",nj)
    return v_o,nj

    
def p_acc(t_in):
    #print("below is  power accelaration chart model")
# Power profile with time
    p_t = [0,5,10,15,20,25,30]
    p_y = [205,210,225,240,260,275,295]

    z = np.polyfit(p_t, p_y, 5)
    f = np.poly1d(z)
    #print(z)
    #print(f)

# calculate new x's and y's
    x_new = np.linspace(p_t[0], p_t[-1], 50)
    y_new = f(x_new)


    #plt.plot(p_t,p_y,'o', x_new, y_new)
    #plt.axis([0,35,200,320])
    #plt.show()


#integratrion
    n=f.integ()
    nj = n(t_in[0])-n(0)
    #print("power conumed in t time accelration ",nj)
    return nj
def v_dec(v_in):
# decelration velocity time and power model

    vd_t =[0,2,4,6,8,10,12,14,15]
    vd_y =[15,14.2,13.2,10.3,7.5,5,3.8,1.2,0]

    z = np.polyfit(vd_t, vd_y, 5)
    f = np.poly1d(z)
    #print(z)
    #print(f(5))

# calculate new x's and y's
    x_new = np.linspace(vd_t[0], vd_t[-1], 50)
    y_new = f(x_new)


    #plt.plot(vd_t,vd_y,'o', x_new, y_new)
    #plt.axis([0,16,0,20])
    #plt.show()
    
#find time value from given velocity value
    hj = v_in-f
    kl = hj.c
    jk =np.roots(kl)
    for v in jk:
        if v <= 0 or v >= 16:
            v = jk
        else:
            v_o = v

    n=f.integ()
    nj = n(15)-n(v_o)
    #print("power conumed in t time accelration ",nj)
    return v_o,nj
    
def p_dec(t_in):
    #print("below is  power deccelaration chart model")
# Power profile with time
    p_t = [0,2,4,6,8,10,12,14,15]
    p_y = [310,240,220,208,212,220,225,230,228]

    z = np.polyfit(p_t, p_y, 5)
    f = np.poly1d(z)
    #print(z)
    #print(f)

# calculate new x's and y's
    x_new = np.linspace(p_t[0], p_t[-1], 50)
    y_new = f(x_new)


    #plt.plot(p_t,p_y,'o', x_new, y_new)
    #plt.axis([0,16,200,320])
    #plt.show() 
    
#integratrion
    n=f.integ()
    nj =n(15)-n(t_in[0])
    #print("power conumed in t time accelration ",nj)
    return nj
    


def c_speed_straight_flight(t_in):
# for different constant speed profile for straight flight
    pfd_t = [0,2,4,5,6,7,8,9,10,10.8,12,13.5,14,15]
    pfd_y = [220,220,217.5,210,205,202,212,215,218,213,250,280,290,335]

    z = np.polyfit(pfd_t, pfd_y, 5)
    f = np.poly1d(z)
   # print(z)
   # print(f)
    p_val = f(t_in)
    return p_val
# calculate new x's and y's
    x_new = np.linspace(pfd_t[0], pfd_t[-1], 50)
    y_new = f(x_new)

    
    #plt.plot(pfd_t,pfd_y,'o', x_new, y_new)
    #plt.axis([0,16,200,360])
    #plt.show()

# Energy Consumed while Climbing
E_climbing = 250         # e/s energy per second while climbiing at 3 m/s speed

#Energy consumed while Descending 

E_Descending = 213

# Energy Consumed while Hovering 

E_Hovering = 210

#Energy Consumed while turning

w_turn = 2.1 # rad/sec
p_turn = 225 #watts/sec
D_angle = 0.2 #rad
E_turn = p_turn*(D_angle/w_turn)

#finding optimal speeds
def optimal_constant_speed():
# Different constant speed ,straight flight and fixed distance. 
    pfvd_t = [2,4,6,8,10,12,12.3,14,16]
    pfvd_y = [110,54,35,28,25,23,22,23,25]

    z = np.polyfit(pfvd_t, pfvd_y, 5)
    f = np.poly1d(z)
    #print(z)
    #print(f)

# calculate new x's and y's
    x_new = np.linspace(pfvd_t[0], pfvd_t[-1], 50)
    y_new = f(x_new)


    #plt.plot(pfvd_t,pfvd_y,'o', x_new, y_new)
    #plt.axis([2,16,20,110])
    #plt.show()


#Variable speed and fixed distances.
distance = [50,100,150,300,600,1200]
power =[]
o_power =[]
speed =[0.2,0.4,0.6,1.0,1.4,1.6,2.0,2.4,2.6,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0]
for j in distance:
    
    for i in speed:
        
        v_val = i
        t_av = v_acc(v_val)  # time to reach the velocity
        p_av = p_acc(t_av) # power consumed by acceleration velocity
        t_dv = v_dec(v_val)    # time to decelerate from the velocity
        p_dv = p_dec(t_dv) # power consumed during decelration velocity
        d_sfl = j - (t_av[1] + t_dv[1]) # distance remaining for straight flight
        t_sfl = d_sfl/v_val    # time for straight flight
        p_sfl = c_speed_straight_flight(v_val) # average value of power for c speed
        tp_sfl = p_sfl * t_sfl
        total_power = p_av + p_dv + tp_sfl
        #print(total_power)
        #print(i)
        power.append(total_power)
    
#print("energy consumed while acc to",v_val, "is", p_av,"and distance cover is",t_av[1])
#print("energy consumed while dec from",v_val, "is", p_dv,"and distance cover is",t_dv[1])
#print("energy consumed straight flight at",v_val, "is", tp_sfl,"and distance cover is",d_sfl)
#print(t_dv)
    z = np.polyfit(speed, power, 10)
    f = np.poly1d(z)
    #print(z)
    #print(f)

# calculate new x's and y's
    x_new = np.linspace(speed[0], speed[-1], 50)
    y_new = f(x_new)

    plt.title('distance= %i'%j, fontsize=16)
    plt.plot(speed,power,'o', x_new, y_new)
    plt.axis()
    plt.show()
    f_d = np.polyder(f)
    hj = f_d-0
    kl = hj.c
    jk =np.roots(kl)
    #mjk = max(jk)
    print("optimal speed ",jk.real)
    o_power.append(jk.real)    

    power = []
"""    
#optimal values from the paper.
o_s = [3.6,6.54,8.08,10.54,11.45,11.87,11.92,12.1,12.1,12.2]
#o_s = [4,7,8,11,11.5,12,12.1]
d_s = [50,100,150,300,600,1200,1500,1600,2000,2100]

z = np.polyfit(d_s, o_s,7)
f = np.poly1d(z)
    #print(z)
    #print(f)

# calculate new x's and y's
x_new = np.linspace(d_s[0], d_s[-1],50)
y_new = f(x_new)

plt.title('optimal speed with distance', fontsize=16)
plt.plot(d_s,o_s,'o', x_new, y_new)
plt.axis([0,1500,0,14])
#plt.axis()
plt.show()    

"""
# main function which calculates according to the path what energy is required
# by the drone. 
climb_speed = 3   # m/s
time_to_reach_max_height = h_max/climb_speed
energy_climbing_desired_height = E_climbing * time_to_reach_max_height
total_straight_distance_of_area = 150 
No_of_turns = 8 
Desc_speed = 4   #m/s
total_e_descending = (h_max/Desc_speed)*E_Descending
e_during_turn = (L_y/4)*217.4    # L_y distance , 4 m/s speed, 217.4 e/s for constant speed flight
t_e_during_turn = (No_of_turns/2)*e_during_turn
dist_straight_single_path= total_straight_distance_of_area/(No_of_turns/2)

speed =[0.2,0.5,1.0,2.0,3,4,5,6,7,8,9,10,11,12]
power =[]

for s in speed:
    distance = dist_straight_single_path  
    v_val = s
    t_av = v_acc(v_val)  # time to reach the velocity
    p_av = p_acc(t_av) # power consumed by acceleration velocity
    t_dv = v_dec(v_val)    # time to decelerate from the velocity
    p_dv = p_dec(t_dv) # power consumed during decelration velocity
    d_sfl = distance - (t_av[1] + t_dv[1]) # distance remaining for straight flight
    t_sfl = d_sfl/v_val    # time for straight flight
    p_sfl = c_speed_straight_flight(v_val) # average value of power for c speed
    tp_sfl = p_sfl * t_sfl
    total_power = p_av + p_dv + tp_sfl
    #print(total_power)
    power.append(total_power.real)



z12 = np.polyfit(speed, power, 10)
f12 = np.poly1d(z12)
    #print(z)
    #print(f)

# calculate new x's and y's
x_new = np.linspace(speed[0], speed[-1], 50)
y_new = f12(x_new)

plt.title('distance= %i'%distance, fontsize=16)
plt.plot(speed,power,'o', x_new, y_new)
plt.axis()
plt.show()
f_d = np.polyder(f12)
hj = f_d-0
kl = hj.c
jk =np.roots(kl)
print("optimal speed for the path")
print(jk.real[6])
y_f12 = f12(jk)
print("optimal energy for one staright patch")
print(y_f12[6])
total_energy_for_all_straight_path = y_f12[6] * (No_of_turns/2)

total_energy_flight = (energy_climbing_desired_height + total_e_descending +
                        t_e_during_turn+ total_energy_for_all_straight_path)

print("energy climbing desired height", energy_climbing_desired_height)
print("total energy descending",total_e_descending)
print("total energy during turns",t_e_during_turn)
print("total energy for all straight_path",total_energy_for_all_straight_path)                       
print("total energy for flight",total_energy_flight.real)






