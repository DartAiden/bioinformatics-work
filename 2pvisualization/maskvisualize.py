import numpy as np
import matplotlib.pyplot as plt
import math
    

a = np.load('stat.npy', allow_pickle=True) #load npy file
curves = []
for i in (a):
#for i in range(1):
    xes = i['xpix']
    yes = i['ypix']
    templist = []
    pairs = np.column_stack((xes,yes))
    for a in range(len(pairs)):
        if not (
            np.any(np.all(pairs == np.array([pairs[a][0] + 1, pairs[a][1]]), axis=1))
            and np.any(np.all(pairs == np.array([pairs[a][0] - 1, pairs[a][1]]), axis=1))
            and np.any(np.all(pairs == np.array([pairs[a][0], pairs[a][1] + 1]), axis=1))
            and np.any(np.all(pairs == np.array([pairs[a][0], pairs[a][1] - 1]), axis=1))
        ):
            templist.append(pairs[a])
    boundary = np.zeros((len(templist),2))
    for i in range(len(templist)):
        boundary[i] = templist[i]
    angles = np.zeros(len(boundary))
    ori = np.array([((np.max(xes) - np.min(xes))/2 + np.min(xes)), ((np.max(yes) - np.min(yes))/2 + np.min(yes))])
    for a in range(len(boundary)):
        angles[a] = np.array([math.atan2(ori[0]-boundary[a][0],ori[1]-boundary[a][1])])
    bas = np.column_stack((boundary,angles))
    sorted_angs = bas[bas[:, 2].argsort()]
    newxes = sorted_angs[:,0]
    newyes = sorted_angs[:,1]
    newxesc = np.pad(newxes, (1,0), 'constant', constant_values = (0))
    newyesc = np.pad(newyes, (1,0), 'constant', constant_values = (0))
    newyesc[0] = newyesc[-1]
    newxesc[0] = newxesc[-1]

    #plt.plot(xes,yes, 'red')
    plt.plot(newxesc,newyesc,'black')
    
plt.show()