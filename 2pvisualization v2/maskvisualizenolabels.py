import numpy as np
import matplotlib.pyplot as plt
import math
import csv

class shape:
    def __init__(self, xes, yes):
        self.xes = xes
        self.yes = yes
        self.cat = None
        self.colors = {None : '#696969', 'male' : '#C80000', 'female' : '#3300FF'}
        self.color = self.colors[self.cat]

    def setcat(self,cat):
        self.cat = cat
        self.color = self.colors[cat]
    def getx(self):
        return self.xes
    def gety(self):
        return self.yes
    def getcolor(self):
        return self.color
    def getcat(self):
            return self.cat


a = np.load('stat.npy', allow_pickle=True) #load npy file
fields = ['initiallabel','category']
data = []
counter = 0
coords = {}
for i in (a):
#for i in range(1):
    xes = i['xpix']
    yes = i['ypix']
    templist = []
    filllist = []
    pairs = np.column_stack((xes,yes))
    for a in range(len(pairs)):
        if not (
            np.any(np.all(pairs == np.array([pairs[a][0] + 1, pairs[a][1]]), axis=1)) #extracts boundary points
            and np.any(np.all(pairs == np.array([pairs[a][0] - 1, pairs[a][1]]), axis=1))
            and np.any(np.all(pairs == np.array([pairs[a][0], pairs[a][1] + 1]), axis=1))
            and np.any(np.all(pairs == np.array([pairs[a][0], pairs[a][1] - 1]), axis=1))
        ):
            templist.append(pairs[a])
        else:
            filllist.append(pairs[a])
    boundary = np.zeros((len(templist),2))
    for i in range(len(templist)): # 
        boundary[i] = templist[i]
    fill = np.zeros((len(filllist),2))
    for i in range(len(filllist)):
        fill[i] = filllist[i]
    fillxes = fill[:,0]
    fillyes = fill[:,1]
    angles = np.zeros(len(boundary))
    ori = np.array([((np.max(xes) - np.min(xes))/2 + np.min(xes)), ((np.max(yes) - np.min(yes))/2 + np.min(yes))]) # estimates the center
    for a in range(len(boundary)):
        angles[a] = np.array([math.atan2(ori[0]-boundary[a][0],ori[1]-boundary[a][1])]) # organizes them by angle
    bas = np.column_stack((boundary,angles)) # adds the column
    sorted_angs = bas[bas[:, 2].argsort()] #sorts by the third column 
    newxes = sorted_angs[:,0] #extracts the angles
    newyes = sorted_angs[:,1]
    newxesc = np.pad(newxes, (1,0), 'constant', constant_values = (0))
    newyesc = np.pad(newyes, (1,0), 'constant', constant_values = (0))
    newyesc[0] = newyesc[-1]
    newxesc[0] = newxesc[-1] # circcularizes them
    datum = {'initiallabel' :counter, 'category' :'null'}
    coords[counter]= shape(newxesc, newyesc)

    #plt.plot(xes,yes, 'red')

    #plt.plot(fillxes, fillyes, 'red')
    #plt.plot(newxesc,newyesc,'black')
    #plt.text(x = np.max(xes) + 4, y =  ((np.max(yes) - np.min(yes))/2 + np.min(yes))-8, s = str(counter), fontsize = 8)
    data.append(datum)
    counter+=1
plt.xticks([])  
plt.yticks([])  
#plt.show()
#plt.clf()


with open('cells.csv', 'r', newline = '') as csvfile:
    reader = csv.DictReader(csvfile)
    counter = 0
    for row in reader:
        if row['category']!= 'null':
            coords[counter].setcat(row['category'])
        counter+=1


plt.xticks([])  
plt.yticks([])
cats = []
labels = []
for i in coords:
    if coords[i].getcat() not in labels:
        plt.plot(coords[i].getx(), coords[i].gety(), c=coords[i].getcolor(), label = coords[i].getcat())
        labels.append(coords[i].getcat())
    else: # this only adds the label if the label has not been used before
        plt.plot(coords[i].getx(), coords[i].gety(), c=coords[i].getcolor())


plt.xticks([])  
plt.yticks([])
plt.legend(loc = 'lower center', bbox_to_anchor = (.5,-.1), ncol = len(colors)-1)
plt.show()
