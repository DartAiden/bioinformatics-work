import numpy as np
import matplotlib.pyplot as plt
import math
    

a = np.load('stat.npy', allow_pickle=True) #load npy file
curves = []
for i in (a):
#for i in range(1):
    xes = i['xpix']
    yes = i['ypix']


    plt.scatter(xes,yes,c='black')
    
plt.show()
