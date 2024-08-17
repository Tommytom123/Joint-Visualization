import matplotlib.pyplot as plt
import numpy as np
import math
import random
from cycler import cycler
import time

plt.style.use('_mpl-gallery')
default_cycler = cycler(color=['r', 'g', 'b', 'y'])
plt.rc('axes', prop_cycle=default_cycler)
random.seed(6789234)

class robotArm2D:
    def __init__(self, startCoordinates = {'x':0,'y':0}, length=2, rotationRadian = math.pi/2, base = True):
        self.subArms = [] 
        self.startCoordinates = startCoordinates
        self.length = length # Hypotenuse
        self.rotationRadian = rotationRadian #Radian from plane {xy (bottom) , xz (side)} (Angle of vector)
        self.endCoordinates = self.calculateEndCoordinates() #x,y,z -> Based off of the length, start coords and Radian from the 2 planes
        self.fig, self.ax = plt.subplots(figsize=(12, 10)) if base else [None,None]

    def calculateEndCoordinates(self):
        x = self.length*math.cos(self.rotationRadian) + self.startCoordinates['x']
        y = self.length*math.sin(self.rotationRadian) + self.startCoordinates['y']
        return {'x':x,'y':y}

    def addArm(self, length = None, rotationRadian = None):
        subArmConstructParams = {
            'startCoordinates': self.endCoordinates if len(self.subArms) == 0 else self.subArms[-1].endCoordinates,
            'base': False
        }
        if length != None:
            subArmConstructParams['length'] = length

        subArmConstructParams['rotationRadian'] = (rotationRadian if rotationRadian != None else 0) + (self.rotationRadian if len(self.subArms) == 0 else self.subArms[-1].rotationRadian)
        subArm = robotArm2D(**subArmConstructParams)
        self.subArms.append(subArm)
        return subArm
    
    def plotArm(self):
        self.ax.plot(self.startCoordinates['x'],self.startCoordinates['y'], marker='o', color='C0')
        self.ax.plot([self.startCoordinates['x'], self.endCoordinates['x']], [self.startCoordinates['y'], self.endCoordinates['y']], color='C0')
        armIdx = 0
        for subArm in self.subArms:
            self.ax.plot(subArm.startCoordinates['x'],subArm.startCoordinates['y'], marker='o', color=f'C{armIdx+1}')
            self.ax.plot([subArm.startCoordinates['x'], subArm.endCoordinates['x']], [subArm.startCoordinates['y'], subArm.endCoordinates['y']], color=f'C{armIdx+1}')
            armIdx += 1
    
    def showPlot(self):

        
        #ax.set(xticklabels=[],yticklabels=[],zticklabels=[])
        #plt.grid(b=None)
        #plt.axis('off')

        #ax.view_init(azim=270, elev=00)
        #plt.set_zlim([0,None])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.ax.clear()
        plt.xlim([-2,8])
        plt.ylim([-2,8])
        time.sleep(0.05)
    #def calculateEndPosistion(self):
        

    def calculateAnglesIK(self, effectorCoordinates):
        self.ax.plot([self.startCoordinates['x'], effectorCoordinates['x']], [self.startCoordinates['y'], effectorCoordinates['y']], color=f'blue', linestyle='--')
        self.ax.plot(effectorCoordinates['x'], effectorCoordinates['y'], color=f'blue', marker='*')
        Angle2 = math.pi-math.acos((pow(self.length,2)+pow(self.subArms[0].length,2)-pow(effectorCoordinates["x"],2)-pow(effectorCoordinates["y"],2))/(2*self.length*self.subArms[0].length))
        Angle1 = math.atan(effectorCoordinates["y"]/effectorCoordinates["x"]) + math.atan((self.subArms[0].length*math.sin(Angle2))/(self.length+(self.subArms[0].length*math.cos(Angle2))))
        self.rotationRadian = Angle1
        self.subArms[0].rotationRadian = -1*Angle2 + Angle1
        self.endCoordinates = self.calculateEndCoordinates()
        self.subArms[0].startCoordinates = self.endCoordinates
        self.subArms[0].endCoordinates = self.subArms[0].calculateEndCoordinates()


roboticAssembly = robotArm2D(length = 3.5)
roboticAssembly.addArm(length=2.5)
#roboticAssembly.addArm(length=2, rotationRadian = (math.pi/4))
plt.ion()

plt.show()
x = 2
y = 2
for i in range(5000):
    x += random.randint(-5,5)/10
    y += random.randint(-5,5)/10
    x = 1 if x < 1 else x
    y = 1 if y < 1 else y
    x = 4 if x > 4 else x
    y = 4 if y > 4 else y
    roboticAssembly.calculateAnglesIK({'x':x,'y':y})
    roboticAssembly.plotArm()
    roboticAssembly.showPlot()
    




"""
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
"""




