import numpy as np
import math 

alpha =  -16.9826330693
beta = 47.9080908756

# ibrav -12
tgac = beta/alpha
angle = math.atan(tgac)
angle_degrees = (angle*360/(2*math.pi) +180)
angle_rad = angle_degrees * math.pi/180
cosangle = math.cos(angle_rad)
c = alpha/cosangle 
print(round(c,5), round(cosangle,5),round(angle_degrees,5) )
