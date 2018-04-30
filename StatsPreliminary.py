# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:56:57 2018

@author: anton
"""

import numpy as np
import matplotlib.pyplot as plt

from math import sqrt
from scipy.stats import wilcoxon, spearmanr

from ReadGroups import (Directory,listFilesLegPositionTrial)
from ReadFiles import ReadFile, lTestCoPKg, lTestCoG


def PrepareSeries(lTest):
    pX = np.zeros(len(lTest))
    pY = np.zeros(len(lTest))
        
    # Split x and y CoP data serie into two difference arrays
    for i in range(len(lTest)):
        pX[i] = lTest[i].X
        pY[i] = lTest[i].Y

    # Normalize values performing difference of serie mean value
    pX[:] = [x - pX.mean() for x in pX]    
    pY[:] = [y - pY.mean() for y in pY]

    # Calculate euclidean position of difference of mean X, Y        
    pp = np.zeros(len(lTest))        
    for i in range(len(lTest)-1):
        pp[i] = sqrt(pX[i]*pX[i] + pY[i]*pY[i])
    
    return pX, pY, pp

def mountSeries(names, which):
    r = []           # Euclidean position of CoP, actually difference of mean
    rx = []          # difference of mean x position (M-L) of CoP
    ry = []          # difference of mean y position (A-P) of CoP

    if which.lower() == "cop":
        i = 0
    else:
        i = 3
        
    for n in names:
        r = np.append(r, names[n][i])
        rx = np.append(rx, names[n][i+1])
        ry = np.append(ry, names[n][i+2])
 
    return r, rx, ry

def mountMean(names, which):
    r = []           # Euclidean position of CoP, actually difference of mean
    rx = []          # difference of mean x position (M-L) of CoP
    ry = []          # difference of mean y position (A-P) of CoP

    if which.lower() == "cop":
        i = 0
    else:
        i = 3
    
    for n in names:
        r = np.append(r, names[n][i].mean())
        rx = np.append(rx, names[n][i+1].mean())
        ry = np.append(ry, names[n][i+2].mean())

    return r, rx, ry
    



def getpXpYSeries(files):
    
    names = {}
        
    for file in files:
        # Read data from file and store into lTestCoP, lTestCoG lists
        ReadFile(Directory, file)
        
        file = file.split('-')
        key = file[1]
        
        pX, pY, pp = PrepareSeries(lTestCoPKg)       
        lTestCoPKg.clear()

        gX, gZ, ppg = PrepareSeries(lTestCoG)
        lTestCoG.clear()

        names[key] = (pp, pX, pY, ppg, gX, gZ)
        
    return names    

# Round down size of related files.
def EqualizeSeries(names1, names2):
    
    for key in names1:        
        #print(key, len(names1[key][0]), len(names2[key][0]))
            
        sizePP = min(len(names1[key][0]), len(names2[key][0]))
        sizePX = min(len(names1[key][1]), len(names2[key][1]))
        sizePY = min(len(names1[key][2]), len(names2[key][2]))
        sizePPG = min(len(names1[key][3]),len(names2[key][3]))
        sizeGX = min(len(names1[key][4]), len(names2[key][4]))
        sizeGZ = min(len(names1[key][5]), len(names2[key][5]))
            
        names1[key] = (names1[key][0][:sizePP],
                      names1[key][1][:sizePX],
                      names1[key][2][:sizePY],
                      names1[key][3][:sizePPG],
                      names1[key][4][:sizeGX],
                      names1[key][5][:sizeGZ])
            
        names2[key] = (names2[key][0][:sizePP],
                      names2[key][1][:sizePX],
                      names2[key][2][:sizePY],
                      names2[key][3][:sizePPG],
                      names2[key][4][:sizeGX],
                      names2[key][5][:sizeGZ])            
        
    return names1, names2

class resultWilcoxon:
    def __init__(self, tp, pp, tpx, ppx, tpy, ppy, tg, pg, tgx, pgx, tgz, pgz):
        self.t_CoP = tp
        self.p_CoP = pp
        self.t_CoPx = tpx
        self.p_CoPx = ppx
        self.t_CoPy = tpy
        self.p_CoPy = ppy
        self.t_CoG = tg
        self.p_CoG = pg
        self.t_CoGx = tgx
        self.p_CoGx = pgx
        self.t_CoGz = tgz
        self.p_CoGz = pgz

class resultSpearmanr:
    def __init__(self, rp, pp, rpx, ppx, rpy, ppy, 
                 rg, pg, rgx, pgx, rgz, pgz,
                 rpg1, ppg1, rpg2, ppg2, 
                 rpg1x, ppg1x, rpg2x, ppg2x,
                 rpg1y, ppg1y, rpg2y, ppg2y):
        self.rho_CoP = rp
        self.p_CoP = pp
        self.rho_CoPx = rpx
        self.p_CoPx = ppx
        self.rho_CoPy = rpy
        self.p_CoPy = ppy
        self.rho_CoG = rg
        self.p_CoG = pg
        self.rho_CoGx = rgx
        self.p_CoGx = pgx
        self.rho_CoGz = rgz
        self.p_CoGz = pgz

        self.rho_CoPG1 = rpg1
        self.p_CoPG1 = ppg1
        self.rho_CoPG2 = rpg2
        self.p_CoPG2 = ppg2
        self.rho_CoPG1x = rpg1x
        self.p_CoPG1x = ppg1x
        self.rho_CoPG2x = rpg2x
        self.p_CoPG2x = ppg2x
        self.rho_CoPG1y = rpg1y
        self.p_CoPG1y = ppg1y
        self.rho_CoPG2y = rpg2y
        self.p_CoPG2y = ppg2y


# differences between two data series of non-parametric data.
def testWilcoxon(pos, trial1, trial2):
        
    files1, files2 = return2Groups(pos, trial1, trial2)        
    names1 = getpXpYSeries(files1)        
    names2 = getpXpYSeries(files2)    

    names1, names2 = EqualizeSeries(names1, names2)
    
    cop1, copx1, copy1 = mountSeries(names1, "cop")
    cop2, copx2, copy2 = mountSeries(names2, "cop")
    cog1, cogx1, cogz1 = mountSeries(names1, "cog")
    cog2, cogx2, cogz2 = mountSeries(names2, "cog")
    
    t_CoP, p_CoP = wilcoxon(cop1, cop2)
    t_CoPx, p_CoPx = wilcoxon(copx1, copx2)
    t_CoPy, p_CoPy = wilcoxon(copy1, copy2)
    t_CoG, p_CoG = wilcoxon(cog1, cog2)    
    t_CoGx, p_CoGx = wilcoxon(cogx1, cogx2)
    t_CoGz, p_CoGz = wilcoxon(cogz1, cogz2)
                              
    return resultWilcoxon(t_CoP, p_CoP, t_CoPx, p_CoPx, t_CoPy, p_CoPy,
            t_CoG, p_CoG, t_CoGx, p_CoGx, t_CoGz, p_CoGz)
 

# Return two filename lists, one related to each specified trial.
# pos = [DS|SS\TS], trial = "A1|A2 ... Z1|Z2"
def return2Groups(pos, trial1, trial2):    
    files1 = listFilesLegPositionTrial(Directory, pos, trial1)
    files1 = list(files1)

    files2 = listFilesLegPositionTrial(Directory, pos, trial2)
    files2 = list(files2)
    
    return files1, files2


# Perform Spearman correlation (non-parametric data)
def testSpearmanr(pos, trial1, trial2):
    files1, files2 = return2Groups(pos, trial1, trial2)
    names1 = getpXpYSeries(files1)
    names2 = getpXpYSeries(files2)
    
    names1, names2 = EqualizeSeries(names1, names2)
    
    cop1, copx1, copy1 = mountSeries(names1, "cop")
    cop2, copx2, copy2 = mountSeries(names2, "cop") 
    cog1, cogx1, cogz1 = mountSeries(names1, "cog")
    cog2, cogx2, cogz2 = mountSeries(names2, "cog") 
        
    rhoCoP, pCoP = spearmanr(cop1, cop2)
    rhoCoPx, pCoPx = spearmanr(copx1, copx2)
    rhoCoPy, pCoPy = spearmanr(copy1, copy2)
    
    rhoCoG, pCoG = spearmanr(cog1, cog2)
    rhoCoGx, pCoGx = spearmanr(cogx1, cogx2)
    rhoCoGz, pCoGz = spearmanr(cogz1, cogz2)
    
    rhoCoPG1, pCoPG1 = spearmanr(cop1, cog1)
    rhoCoPG2, pCoPG2 = spearmanr(cop2, cog2)

    rhoCoPG1x, pCoPG1x = spearmanr(copx1, cogx1)
    rhoCoPG2x, pCoPG2x = spearmanr(copx2, cogx2)

    rhoCoPG1y, pCoPG1y = spearmanr(copy1, cogz1)
    rhoCoPG2y, pCoPG2y = spearmanr(copy2, cogz2)

    return resultSpearmanr(rhoCoP, pCoP, rhoCoPx, pCoPx, rhoCoPy, pCoPy,
                           rhoCoG, pCoG, rhoCoGx, pCoGx, rhoCoGz, pCoGz,
                           rhoCoPG1, pCoPG1, rhoCoPG2, pCoPG2,
                           rhoCoPG1x, pCoPG1x, rhoCoPG2x, pCoPG2x,
                           rhoCoPG1y, pCoPG1y, rhoCoPG2y, pCoPG2y)

def Bland_Altman_plot(title, data1, data2, *args, **kwargs):
    data1     = np.asarray(data1)
    data2     = np.asarray(data2)
    mean      = np.mean([data1, data2], axis=0)
    diff      = data1 - data2                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference
    
    plt.scatter(mean, diff, *args, **kwargs)
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
    plt.xlabel("Average of two measures")
    plt.ylabel("Difference between two measures")
    plt.title("Bland-Altman plot " + title)
    plt.show()
    

#
# parameter:  method (CoG|CoP), group (group1|group2), trials (A1|A2)
def TestsAggreement(parameter):
    
    if parameter == "method":
        files1, files2 = return2Groups(position, trial1, trial2)
        names1 = getpXpYSeries(files1)        
        names2 = getpXpYSeries(files2)
        
        names1, names2 = EqualizeSeries(names1, names2)
        
        cop1, copx1, copy1 = mountSeries(names1, "cop")
        cop2, copx2, copy2 = mountSeries(names2, "cop")
        cog1, cogx1, cogz1 = mountSeries(names1, "cog")
        cog2, cogx2, cogz2 = mountSeries(names2, "cog")
        
        meanCoP1, meanCoPX1, meanCoPY1 = mountMean(names1, "cop")
        meanCoP2, meanCoPX2, meanCoPY2 = mountMean(names2, "cop")
                
        Bland_Altman_plot(position + " CoP Euclidean intragroup all", cop1, cop2)
        Bland_Altman_plot(position + " CoP Euclidean intragroup mean", meanCoP1, meanCoP2)
        
        Bland_Altman_plot(position + " CoPx intragoup all", copx1, copx2)
        Bland_Altman_plot(position + " CoPx intragoup mean", meanCoPX1, meanCoPX2)
        
        Bland_Altman_plot(position + " CoPy intragoup all", copy1, copy2)
        Bland_Altman_plot(position + " CoPy intragoup mean", meanCoPY1, meanCoPY2)

        Bland_Altman_plot(position + " CoG Euclidean intragroup", cog1, cog2)
        Bland_Altman_plot(position + " CoGx intragoup", cogx1, cogx2)
        Bland_Altman_plot(position + " CoGz intragoup", cogz1, cogz2)


            
position = "TS"
trial1 = "A1"
trial2 = "A2"

TestsAggreement("method")



"""
r = testWilcoxon(position, trial1, trial2)

title = "Wilcoxon test - " + trial1 + " vs " + trial2 + "\nAll participants - "

if position == "DS":
    title += "Double Stance Leg"
elif position == "SS":
    title += "Single Stance Leg"
else:
    title += "Tandem Stance Leg"

print(title)
print("CoP  t = %2.0f \tp = %2.5f" %(r.t_CoP, r.p_CoP))
print("CoG  t = %2.0f\tp = %2.5f\n" %(r.t_CoG, r.p_CoG))

print("CoP X  t = %2.0f\tp = %2.5f" %(r.t_CoPx, r.p_CoPx))
print("CoP Y  t = %2.0f\tp = %2.5f\n" %(r.t_CoPy, r.p_CoPy))
print("CoG X  t = %2.0f\tp = %2.5f" %(r.t_CoGx, r.p_CoGx))
print("CoG Z  t = %2.0f\tp = %2.5f\n" %(r.t_CoGz, r.p_CoGz))


r = testSpearmanr(position, trial1, trial2)

title = "Spearmanr test - " + trial1 + " vs " + trial2 + "\nAll participants - "

if position == "DS":
    title += "Double Stance Leg"
elif position == "SS":
    title += "Single Stance Leg"
else:
    title += "Tandem Stance Leg"



print(title)
print("Trial 1 versus Trial2")
print("CoP  t = %2.4f \tp = %2.5f" %(r.rho_CoP, r.p_CoP))
print("CoP X  t = %2.4f\tp = %2.5f" %(r.rho_CoPx, r.p_CoPx))
print("CoP Y  t = %2.4f\tp = %2.5f\n" %(r.rho_CoPy, r.p_CoPy))

print("CoG  t = %2.4f\tp = %2.5f" %(r.rho_CoG, r.p_CoG))
print("CoG X  t = %2.4f\tp = %2.5f" %(r.rho_CoGx, r.p_CoGx))
print("CoG Z  t = %2.4f\tp = %2.5f\n" %(r.rho_CoGz, r.p_CoGz))

print("Center of Pressure versus Center of Gravity")
print("CoP vs CoG trial-1  t = %2.4f\tp = %2.5f" %(r.rho_CoPG1, r.p_CoPG1))
print("CoP vs CoG trial-2  t = %2.4f\tp = %2.5f\n" %(r.rho_CoPG2, r.p_CoPG2))


print("CoP X vs CoG X trial-1  t = %2.4f\tp = %2.5f" %(r.rho_CoPG1x, r.p_CoPG2x))
print("CoP X vs CoG X trial-2  t = %2.4f\tp = %2.5f\n" %(r.rho_CoPG2x, r.p_CoPG2x))

print("CoP Y vs CoG Z trial-1  t = %2.4f\tp = %2.5f" %(r.rho_CoPG1y, r.p_CoPG2y))
print("CoP Y vs CoG Z trial-2  t = %2.4f\tp = %2.5f\n" %(r.rho_CoPG2y, r.p_CoPG2y))
"""
