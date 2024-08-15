import matplotlib.pyplot as plt
import numpy as np
import math
import random
from cycler import cycler
plt.style.use('_mpl-gallery')
default_cycler = cycler(color=['r', 'g', 'b', 'y'])
plt.rc('axes', prop_cycle=default_cycler)
random.seed(6789234)

class robotArm:
    def __init__(self, startCoordinates = {'x':0,'y':0,'z':0}, length=2, posRadian = {'xy': (math.pi/2), 'xz':0}):
        self.subArms = [] 
        self.startCoordinates = startCoordinates
        self.length = length # Hypotenuse
        self.posRadian = posRadian #Radian from plane {xy (bottom) , xz (side)} (Angle of vector)
        self.endCoordinates = self.calculateEndCoordinates() #x,y,z -> Based off of the length, start coords and Radian from the 2 planes
        
    def calculateEndCoordinates(self):
        z = self.length*math.sin(self.posRadian['xy']) + self.startCoordinates['z']
        xyHypotenuse = self.length*math.cos(self.posRadian['xy'])
        x = xyHypotenuse*math.cos(self.posRadian['xz']) + self.startCoordinates['x']
        y = xyHypotenuse*math.sin(self.posRadian['xz']) + self.startCoordinates['y']
        return {'x':x,'y':y,'z':z}

    def addArm(self, length=2, posRadian = {'xy': (math.pi/2), 'xz':0}):
        subArm = robotArm(self.endCoordinates if len(self.subArms) == 0 else self.subArms[-1].endCoordinates, length, posRadian)
        self.subArms.append(subArm)
        return subArm
    
    def plotArm(self):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(12, 10))
        ax.plot(self.startCoordinates['x'],self.startCoordinates['y'],self.startCoordinates['z'], marker='o', color='C0')
        ax.plot([self.startCoordinates['x'], self.endCoordinates['x']], [self.startCoordinates['y'], self.endCoordinates['y']], [self.startCoordinates['z'], self.endCoordinates['z']], color='C0')
        armIdx = 0
        for subArm in self.subArms:
            ax.plot(subArm.startCoordinates['x'],subArm.startCoordinates['y'],subArm.startCoordinates['z'], marker='o', color=f'C{armIdx+1}')
            ax.plot([subArm.startCoordinates['x'], subArm.endCoordinates['x']], [subArm.startCoordinates['y'], subArm.endCoordinates['y']], [subArm.startCoordinates['z'], subArm.endCoordinates['z']], color=f'C{armIdx+1}')
            armIdx += 1
        #ax.set(xticklabels=[],yticklabels=[],zticklabels=[])
        #plt.grid(b=None)
        #plt.axis('off')
        plt.xlim([0,5])
        plt.ylim([0,5])
        ax.view_init(azim=270, elev=00)
        #plt.set_zlim([0,None])
        plt.show()

roboticAssembly = robotArm(length = 1)
roboticAssembly.addArm(length=2, posRadian = {'xy': (random.random()*(math.pi/2)), 'xz':0})
#roboticAssembly.addArm(length=3, posRadian = {'xy': (random.random()*(math.pi/2)), 'xz':0})
#roboticAssembly.addArm(length=2, posRadian = {'xy': (random.random()*(math.pi/2)), 'xz':0})
roboticAssembly.plotArm()





