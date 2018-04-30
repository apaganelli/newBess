# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 17:14:11 2018

@author: Antonio Iyda Paganelli

Next: perform comparisons between first and second trial for all participants
in each position.

"""
from ReadGroups import (listFilesLegPosition, Directory, ConsolidatedResults, 
                        listFilesLegPositionTrial)
from ReadFiles import ReadFile, lTestCoPKg, lTestCoG, PrintResults, StdData

import cmocean
import matplotlib.pyplot as plt
import numpy as np

def plotStatoCinesiogram(X, Y, title):
    plt.plot(X, Y, '.')
    plt.xlabel("Medial-Lateral (mm)")
    plt.ylabel("Antero-Posterior (mm)")
    plt.title(title)
    plt.show()
    plt.clf()
    plt.gcf().clear()
    

def plotStabilogram(T, X, Y, title):
    plt.plot(T, X, label="M-L")
    plt.plot(T, Y, label="A-P")
    plt.xlabel("Time in sec")
    plt.ylabel("Displacement in mm")
    plt.title(title)
    plt.legend()
    plt.show()
    plt.clf()
    plt.gcf().clear()
    
def plotHistogram(X, title):
    legBins = np.arange(-11, 11, 0.5)
    plt.hist(X, legBins)
    plt.title(title)
    plt.show()
    plt.clf()
    plt.gcf().clear()

#
# Use min and max for DS
# Use -51 +51 for SS
# 
#
def plotHistColor(pX, pY, title):
    """
    Only use if necessary to find reasonable ranges.
    xMin = int(pX.min())
    yMin = int(pY.min())
    xMax = int(pX.max())
    yMax = int(pY.max())
    
    if xMin < yMin:
        minEdge = xMin
    else:
        minEdge = yMin
        
    if xMax > yMax:
        maxEdge = xMax
    else:
        maxEdge = yMax
     
    step = 1
    x = np.arange(minEdge - 2*step, maxEdge + 2*step, step)
    y = np.arange(minEdge - 2*step, maxEdge + 2*step, step)
        """    
    stepY = 1
    stepX = 1
    edge = 51
    x = np.arange(-edge, edge, stepX)
    y = np.arange(-edge, edge, stepY)
    minEdgeX = -edge
    minEdgeY = -edge
        
    X, Y = np.meshgrid(x, y)
    
    data = [[0]*len(x)] * len(y)
    data = np.array(data)
    
    for i in range(len(pY)):
        pos_y = int(pY[i]/stepY) + abs(int(minEdgeY/stepY))                
        pos_x = int(pX[i]/stepX) + abs(int(minEdgeX/stepX))
           
        if(pos_x >= len(x) or pos_y >= len(y) or pos_y < 0 or pos_x < 0):
        #print(pos_y, pos_x, i, j, pY[i], pX[j], minEdge, np.shape(data))
            continue
        else:
            data[pos_y, pos_x] += 1            
    
    print(np.shape(data))
    
    minScale = data.min()
    maxScale = data.max()
        
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_title(title)
    im = ax.pcolormesh(X,Y, data, cmap='inferno_r', vmin=minScale, vmax=maxScale)    
    #im = ax.pcolormesh(X,Y, data, cmap=cmocean.cm.ice_r, vmin=minScale, vmax=maxScale)
    plt.colorbar(im)
    plt.show()
    
###############################################################################
position = "TS"
#trial = "A2"


#files = listFilesLegPositionTrial(Directory, position, trial)
files = listFilesLegPosition(Directory, position)
files = list(files)

lCoPX = np.array(0)
lCoGX = np.array(0)
lCoPY = np.array(0)
lCoGZ = np.array(0)
lres = []

j = 1

for file in files:
    ReadFile(Directory, file)

    print("Filename " + file + " #frames " + str(len(lTestCoPKg)))

    pT = []
    pX = np.zeros(len(lTestCoPKg))
    pY = np.zeros(len(lTestCoPKg))

    for i in range(len(lTestCoPKg)):
        pX[i] = lTestCoPKg[i].X
        pY[i] = lTestCoPKg[i].Y

    pX[:] = [x - pX.mean() for x in pX]    
    pY[:] = [y - pY.mean() for y in pY]
    
    #file = file.split('.')
    #plotHistColor(pX, pY, "CoP " + file[0])            
    #plotStatoCinesiogram(pX, pY, "CoP behaivour - " + position )
    #plotStabilogram(pT, pX, pY, "Stabilogram - CoP - " + position)

    #plotHistogram(pX, "Histogram CoP - X - " + position)
    #plotHistogram(pY, "Histogram CoP - Y - " + position)
    result = StdData(lTestCoPKg, 2)
    #PrintResults(result, 2)
    lres.append(result)

    lCoPX = np.append(lCoPX, pX)
    lCoPY = np.append(lCoPY, pY)
    lTestCoPKg.clear()
     
    gT = []
    gX = np.zeros(len(lTestCoG))
    gZ = np.zeros(len(lTestCoG))

    for i in range(len(lTestCoG)):
        gT.append(lTestCoG[i].Time / 1000)
        gX[i] = lTestCoG[i].X
        gZ[i] = lTestCoG[i].Z
        
    gX[:] = [x - gX.mean() for x in gX]    
    gZ[:] = [z - gZ.mean() for z in gZ]        

    #file = file.split('-')
    #title = position + " " + file[1] + " " + str(j)
    #plotStatoCinesiogram(gX, gZ, title)
    #plotHistogram(gX, "Histogram CoG M-L(X) " + title)
    #plotHistogram(gZ, "Histogram CoG A-P(Y) " + title)
    #plotStabilogram(gT, gX, gZ, "Stabilogram - CoG " + title)

    #result = StdData(lTestCoG, 3)
    #PrintResults(result, 3)    
    #lres.append(result)

    lCoGX = np.append(lCoGX, gX)
    lCoGZ =  np.append(lCoGZ, gZ)
    lTestCoG.clear()
    j += 1

if position == "DS":
    title = "Double Stance Leg"
elif position == "SS":
    title = "Single Stance Leg"
else:
    title = "Tandem Stance Leg"


plotHistColor(lCoPX, lCoPY, "Color Map Histogram CoP - " + title + "\nAll Participants ")
#plotStatoCinesiogram(lCoPX, lCoPY, "CoP behaivour %d" %j)
#plotStabilogram(gT, gX, gY, "Stabilogram - CoG %d" %j)

#plotHistogram(lCoPX, "Total CoP X")
#plotHistogram(lCoPY, "Total CoP Y")

#plotHistogram(lCoGX, "Total ALL CoG M-L (X) " + position)
#plotHistogram(lCoGZ, "Total ALL CoG A-P (Y) " + position)
plotHistColor(lCoGX, lCoGZ, "Color Map Histogram CoG " + position + "\nAll Participants")

ConsolidatedResults(lres, "2D")   