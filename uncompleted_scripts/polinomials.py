import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func(I,x0,a,b,c,d,e):
    x,y = I
    return x0 + a*x + b*y + c*x*y +d*x*x + e*y*y

xdata = np.loadtxt('J1.txt')[:, 0]
ydata = np.loadtxt('J1.txt')[:, 1]
zdata = np.loadtxt('J1.txt')[:, 2]
#coef = np.array([0,0,0,0]);trash = np.array([0,0,0,0]);trash_matrix = np.zeros((4,3))
coef = np.array([0,0,0,0,0,0]);trash = np.array([0,0,0,0,0,0]);trash_matrix = np.zeros((6,3))
res = curve_fit(func, (xdata,ydata), zdata)
x0 = res[0][0]; a = res[0][1]; b = res[0][2]; c = res[0][3]; d = res[0][4]; e = res[0][5]
#print(xdata)
#print(x0,a,b,c,d,e)


x = np.array([])
y = np.array([])
z = np.array([])
#figsimple,ax = plt.subplots() 
#ax.plot(y,x0  + b*y ,'bo')
#plt.savefig('simple.png')

for i in range(95,105,1):
    for j in range(2,3,1):
        #print(i,j,x0 + a*i + b*j + c*i*j)
        x = np.append(x,i)
        y = np.append(y,j)
        z = np.append(z,x0 + a*i + b*j + c*i*j +d*i*i + e*j*j)
#print(x)
#print(y)
#print(z)

figsimple,ax = plt.subplots() 
ax.plot(x,z ,'bo')
plt.savefig('simple.png')
