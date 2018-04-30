# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 11:01:25 2018

@author: Antonio Iyda Paganelli
Master Project - BESS Balance Board Analysis

Group analysis
"""

import os
from RawData import Build_CoP_from_RawData
from ReadFiles import (ReadFile, StdData, PrintResults, 
                       lTestCoPKg, lTestCoG)

from Classes import (StdResults2D, StdResults3D)

def listFiles(Dir):
    for file in os.listdir(Dir):
        if os.path.isfile(os.path.join(Dir, file)) and \
        ("DS" in file[0:2] or "SS" in file[0:2] or "TS" in file[0:2]):
            yield file
            
def listFilesLegPosition(Dir, position):
    for file in os.listdir(Dir):
        if os.path.isfile(os.path.join(Dir, file)) and \
        (position in file[0:6]):
            yield file
            
def listFilesLegPositionTrial(Dir, position, trial):    
    if position.lower() == "all":
        position = "S"
    
    for file in os.listdir(Dir):
        # filename: [DS|SS|TS]-Name-[An|...|Zn]-YYYY-MM-DD-HH_mm_SS.txt
        # An..Zn - trial identification, i.e. A1, Z3.
        parts = file.split('-')
        
        if os.path.isfile(os.path.join(Dir, file)) and \
        (position in file[0:2]) and (trial in parts[2]):
            yield file
       
def ConsolidatedResults(lResults, dim):
    j = len(lResults)
    
    if dim == "2D":
        r = StdResults2D(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    else:
        r = StdResults3D(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0)

    for lr in lResults:
        r.MinX += lr.MinX
        r.MaxX += lr.MaxX
        r.AmpX += lr.AmpX
        r.MinY += lr.MinY
        r.MaxY += lr.MaxY
        r.AmpY += lr.AmpY

        r.MeanX   += lr.MeanX
        r.StdDevX += lr.StdDevX
        r.RMSX    += lr.RMSX
        r.MeanY   += lr.MeanY    
        r.StdDevY += lr.StdDevY
        r.RMSY    += lr.RMSY
        r.NormalX += lr.NormalX
        r.NormalY += lr.NormalY
        
        if dim == "3D":
            r.MinZ += lr.MinZ
            r.MaxZ += lr.MaxZ
            r.AmpZ += lr.AmpZ
            r.MeanZ   += lr.MeanZ
            r.StdDevZ += lr.StdDevZ
            r.RMSZ    += lr.RMSZ
            r.NormalZ += lr.NormalZ
            
        r.TotalPathLen += lr.TotalPathLen
        r.PeakVel += lr.PeakVel
        r.AvgVel += lr.AvgVel

    print("Consolidated results (mean) %d" %j)

    r.MinX /= j
    r.MaxX /= j
    r.AmpX /= j
    r.MinY /= j
    r.MaxY /= j
    r.AmpY /= j
    r.MeanX   /= j
    r.StdDevX /= j
    r.RMSX    /= j
    r.MeanY   /= j
    r.StdDevY /= j
    r.RMSY    /= j    
    r.NormalX /= j
    r.NormalY /= j
    r.TotalPathLen /= j
    r.PeakVel      /= j
    r.AvgVel       /= j
    
    if dim == "3D":
        r.MinZ /= j
        r.MaxZ /= j
        r.AmpZ /= j
        r.MeanZ   /= j
        r.StdDevZ /= j
        r.RMSZ    /= j
        r.NormalZ /= j
        PrintResults(r, 3)
    else:     
        PrintResults(r, 2)



#################################################################################
Directory = "C:\\Users\\anton\\source\\repos\\NewBess\\NewBess\\bin\\x64\\Debug\Data\\"


"""
files = listFilesLegPosition(Directory, "DS")

AllCoPKg = []
lResultsCoP = []
lResultsNewCoP = []
lResultsCoG = []

j = 0
for file in files:
    ReadFile(Directory, file)
    
    # Get standard results & print them
    result = StdData(lTestCoPKg, 2)
    PrintResults(result, 2)
    
    # Save each individual result    
    lResultsCoP.append(result)    

    # Append data series all together.
    # AllCoPKg += lTestCoPKg
    
    # Clean up data serie.
    lTestCoPKg.clear()
    
    result = StdData(lTestCoG, 3)
    PrintResults(result, 3)
    
    lResultsCoG.append(result)
    lTestCoG.clear()
        
    j += 1


print("Center of Pressure")
ConsolidatedResults(lResultsCoP)

print ("Center of Gravity")
ConsolidatedResults(lResultsCoG)
"""    
    