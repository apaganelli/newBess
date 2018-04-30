# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 23:53:22 2018

@author: anton

Read research files.
There are three types of files, one for each position (DS, SS, TS)

Rule of filename formation:
    
FileType-UserName-TestID-YYYY-MM-DD-HH_MM_SS.TXT

"""

import sys
import math
import numpy as np
import scipy.stats as stats
from Classes import (RawLoadCell, Raw2DTimePoint, 
                     Raw3DTimePoint, StdResults2D, StdResults3D, 
                     JointPosition, Eyes, BodyFrame)

from RawData import Build_CoP_from_RawData

#
# Min, Max, Mean, StdDev, RMS, Amplitude
#
def StdData(DataSerie, axis):
    length = len(DataSerie)
        
    dataX = np.zeros(length)
    dataY = np.zeros(length)

    if(axis == 3):
       dataZ = np.zeros(length) 
       RMS_Z = 0

    RMS_X = 0
    RMS_Y = 0
    
    for i in range(length):
        dataX[i] = DataSerie[i].X
        dataY[i] = DataSerie[i].Y
        RMS_X += (dataX[i] * dataX[i])
        RMS_Y += (dataY[i] * dataY[i])
        if(axis == 3):
            dataZ[i] = DataSerie[i].Z
            RMS_Z += (dataZ[i] * dataZ[i])
        
    RMS_X = math.sqrt(RMS_X / length)
    RMS_Y = math.sqrt(RMS_Y / length)        
    Mean_X = dataX.mean()
    Mean_Y = dataY.mean()    
    StdDev_X = dataX.std()
    StdDev_Y = dataY.std()
    
    if(axis == 3):
        RMS_Z = math.sqrt(RMS_Z / length)
        Mean_Z = dataZ.mean()
        StdDev_Z = dataZ.std()
        zAnt = dataZ[0]
        Min_Z = dataZ.min()
        Max_Z = dataZ.max()
    
    Min_X = dataX.min()
    Max_X = dataX.max()    
    Min_Y = dataY.min()
    Max_Y = dataY.max()
        
    TotalPathLength = 0
    distance = 0    
    PeakVelocity = sys.float_info.min
    vel = sys.float_info.min
    
    timeAnt = DataSerie[0].Time
    initialTime = timeAnt
    xAnt = dataX[0]
    yAnt = dataY[0]
    
    meanTimeFreq = 0
            
    for i in range(len(dataX)):
        
        if(i < len(dataX)-1):
            meanTimeFreq += (DataSerie[i+1].Time - DataSerie[i].Time)

        x = dataX[i]
        
        if(axis == 2):
            y = dataY[i]
        else:
            z = dataZ[i]
            
        while (x > (Mean_X + (StdDev_X * 5))) or (x < (Mean_X - (StdDev_X * 5))):
            x = (x + Mean_X) / 2;
                
        dataX[i] = x;
        
        if(axis == 2):
            while (y > (Mean_Y + (StdDev_Y * 5))) or (y < (Mean_Y - (StdDev_Y * 5))):
                y = (y + Mean_Y) / 2;
                
            dataY[i] = y;            
            distance = math.sqrt(math.pow(dataX[i] - xAnt, 2) + math.pow(dataY[i] - yAnt, 2));
            yAnt = dataY[i]
        else:    
            while (z > (Mean_Z + (StdDev_Z * 5))) or (z < (Mean_Z - (StdDev_Z * 5))):
                z = (z + Mean_Z) / 2;
                
            dataZ[i] = z;            
            distance = math.sqrt(math.pow(dataX[i] - xAnt, 2) + math.pow(dataZ[i] - zAnt, 2));
            zAnt = dataZ[i]

        if(DataSerie[i].Time - timeAnt > 0):
            vel = (distance / 1000) / ((DataSerie[i].Time - timeAnt) / 1000) 
        
        if(vel > 100):
            print("i of DataSerie %d  %2.4f %2.4f %4.2f  %4.2f" %(i, DataSerie[i].Time, timeAnt, distance, vel))
        
        if vel > PeakVelocity and not math.isinf(vel):
            PeakVelocity = vel
        
        xAnt = dataX[i]                
        TotalPathLength += distance;
        timeAnt = DataSerie[i].Time


    AvgVelocity = (TotalPathLength / 1000) / ((timeAnt - initialTime) / 1000)

    z, pX = stats.shapiro(dataX)
    z, pY = stats.shapiro(dataY)

    if(axis == 3):
        z, pZ = stats.shapiro(dataZ)
        result = StdResults3D(Min_X, Max_X, Mean_X, StdDev_X, RMS_X, pX,
                            Min_Y, Max_Y, Mean_Y, StdDev_Y, RMS_Y, pY,
                            Min_Z, Max_Z, Mean_Z, StdDev_Z, RMS_Z, pZ,
                            TotalPathLength, PeakVelocity, AvgVelocity)
    else:
        result = StdResults2D(Min_X, Max_X, Mean_X, StdDev_X, RMS_X, pX,
                            Min_Y, Max_Y, Mean_Y, StdDev_Y, RMS_Y, pY,
                            TotalPathLength, PeakVelocity, AvgVelocity)            
        
        
    meanTimeFreq /= len(DataSerie)
    
    print("Mean frame time: %3.0f ms / %2.1f Hz  " %(meanTimeFreq, 1000/meanTimeFreq))
    
    return result


def PrintResults(r, axis):
    print("Total Path length: %5.1f" %r.TotalPathLen)
    print("Peak Velocity: %5.3f\nAverage Velocity:  %5.3f\n" %(r.PeakVel, r.AvgVel))
    
    print("[X] Min,  Max, Amplitude: %4.2f \t %4.2f \t %4.2f" %(r.MinX, r.MaxX, r.AmpX))
    print("[X] Mean, StdDev, RMS:    %4.2f \t %4.2f \t %4.2f" %(r.MeanX, r.StdDevX, r.RMSX))
    
    if(r.NormalX < 0.055):
        print("[X] NOT normally distributed. p = %3.5f\n" %(r.NormalX))
    else:
        print("[X] normally distributed.\n")
        
    print("[Y] Min, Max, Amplitude: %4.2f \t %4.2f \t %4.2f" %(r.MinY, r.MaxY, r.AmpY))
    print("[Y] Mean, StdDev, RMS:   %4.2f \t %4.2f \t %4.2f" %(r.MeanY, r.StdDevY, r.RMSY))
    
    if(r.NormalY < 0.055):
        print("[Y] NOT normally distributed. p = %3.5f\n" %(r.NormalY))
    else:
        print("[Y] normally distributed.\n")
    
    if(axis == 3):
        print("[Z] Min,  Max, Amplitude: %4.2f \t %4.2f \t %4.2f" %(r.MinZ, r.MaxZ, r.AmpZ))
        print("[Z] Mean, StdDev, RMS:    %4.2f \t %4.2f \t %4.2f" %(r.MeanZ, r.StdDevZ, r.RMSZ))
    
        if(r.NormalZ < 0.055):
            print("[Z] NOT normally distributed. p = %3.5f\n" %(r.NormalZ))
        else:
            print("[Z] normally distributed.\n")
            
###########################################################################
Directory = "C:\\Users\\anton\\source\\repos\\BESS\\BESS\\bin\\x64\\Debug\Data\\"
#Filename = "DS-Antonio-A2-2018-04-17-10_55_46.txt"
Filename = "DS-Antonio-B2-2018-04-17-11_24_08.txt"

lZeroCal = []
lCalibrationCoP = []
lCalibrationCoG = []
lCalibrationWii = []
lBodyCal = []
lBodyTest = []
lTestCoP = []
lTestCoPKg = []
lTestCoG = []
lTestWii = []
lTestWiiKg = []
lEyes = []
zeroCal = Cal0 = Cal17 = Cal34 = RawLoadCell(0,0,0,0,0)


def ReadFile(Directory, Filename):        
    Name = Directory + Filename
    timeTestCoP = 0
    timeTestCoPKg = 0

    ZeroCalibration = False
    Calibration = False
    Test = False
    Joints3DCal = False
    Joints3DTest = False

    lastEyeTime = ""
    
    with open(Name, 'rt') as f:
        for line in f:
            line = line[:-1]
            line = line.replace(",", ".")
            line = line.split(":")
            # starts file with #Start ZeroCalibration
            # Fields:  RL-0Cal:BL:BR:TL:TR
            #          CAL0_17_34: for each weight BL,BR,TL,TR        
            # ends with field1 == CAL0_17_34
        
            if "#Start ZeroCalibration" in line[0]:
                ZeroCalibration = True
                continue
            elif "#Start calibration" in line[0]:
                Calibration = True
                ZeroCalibration = False
                continue
                
            if ZeroCalibration:
                line = [l.replace(".", "") for l in line]
            
                if line[0] == "RL-0Cal":
                    zeroCal = RawLoadCell(float(line[1]), float(line[2]), float(line[3]), float(line[4]), 0)
                    lZeroCal.append(zeroCal)                        
                else:
                    # Stores for each weight BL, BR, TL, TR                                
                    Cal0 = RawLoadCell(float(line[1]), float(line[2]), float(line[3]), float(line[4]), 0)
                    Cal17 = RawLoadCell(float(line[5]), float(line[6]), float(line[7]), float(line[8]), 0)
                    Cal34 = RawLoadCell(float(line[9]), float(line[10]), float(line[11]), float(line[12]), 0)
                    ZeroCalibration = False
                    continue

            # next section:  #Start Calibration
            if Calibration:
                if line[0] == "CoP":
                    line = [l.replace(".", "") for l in line]
                    timeCalCoP = float(line[1])
                    obj = Raw2DTimePoint(timeCalCoP, float(line[2]), float(line[3]))
                    lCalibrationCoP.append(obj)
                elif line[0] == "CoM":
                    obj = Raw3DTimePoint(float(line[1]), float(line[2]), float(line[3]), float(line[4]))
                    lCalibrationCoG.append(obj)
                elif line[0] == "RL":
                    RL = RawLoadCell(float(line[1]), float(line[2]), float(line[3]), float(line[4]), timeCalCoP)
                    lCalibrationWii.append(RL)
                else:
                    Calibration = False
                    Test = True
                    continue
        
            # next section:  #Start Test
            if Test:
                if line[0] == "CoP":
                    line = [l.replace(".", "") for l in line]
                    timeTestCoP = float(line[1])
                    CoP = Raw2DTimePoint(timeTestCoP, float(line[2]), float(line[3]))
                    lTestCoP.append(CoP)
                elif line[0] == "CoP-Kg":
                    line[1] = line[1].replace(".", "")
                    timeTestCoPKg = float(line[1])
                    CoP = Raw2DTimePoint(timeTestCoPKg, float(line[2]), float(line[3]))
                    lTestCoPKg.append(CoP)
                elif line[0] == "CoM":
                    # Time (ms), X, Y, Z in meters - then converted to mm.
                    CoM = Raw3DTimePoint(float(line[1]), float(line[2]) * 1000 , float(line[3]) * 1000, float(line[4]) * 1000)
                    lTestCoG.append(CoM)
                elif line[0] == "RL":
                    line = [l.replace(".", "") for l in line]
                    RL = RawLoadCell(float(line[1]), float(line[2]), float(line[3]), float(line[4]), timeTestCoP)
                    lTestWii.append(RL)
                elif line[0] == "RL-Kg":
                    RL = RawLoadCell(float(line[1]), float(line[2]), float(line[3]), float(line[4]), timeTestCoPKg)
                    lTestWiiKg.append(RL)
                elif line[0] == "EYES":                
                    if(line[1] == lastEyeTime):
                        continue
                
                    if("OPEN" in line[2]):
                        status = "O"
                    else:
                        status = "C"
                
                    eyes = Eyes(line[1], status)
                    lEyes.append(eyes)
                elif line[0] == "EyesError":
                    pass
                elif line[0] == "JointError":
                    pass
                elif line[0] == "Finished":
                    pass
                elif line[0] == "#Start Joints3D Calibration":
                    Test = False
                    Joints3DCal = True
                    continue
                
            # next section: #Start Joints3D Calibration
            if Joints3DCal:
                if line[0] == "#Start Joints3D Test":
                    Joints3DCal = False
                    Joints3DTest = True
                    continue
                else:
                    bodyCal = BodyFrame(line[0])                
                    i = 1
                    while(i < 126):
                        joint = JointPosition(line[i], line[i+1], line[i+2], line[i+3], line[i+4])
                        bodyCal.Joints.append(joint)                
                        i = i + 5
                
                    lBodyCal.append(bodyCal)                
                
            # next section: #Start Joints3D Test
            if Joints3DTest:
                bodyTest = BodyFrame(line[0])               
                i = 1
                while(i < 126):
                    joint = JointPosition(line[i], line[i+1], line[i+2], line[i+3], line[i+4])
                    bodyTest.Joints.append(joint)                
                    i = i + 5      
                    
                lBodyTest.append(bodyTest)                                    

    zeroCal.BL = sum(a.BL for a in lZeroCal) / len(lZeroCal)
    zeroCal.BR = sum(a.BR for a in lZeroCal) / len(lZeroCal)
    zeroCal.TL = sum(a.TL for a in lZeroCal) / len(lZeroCal)
    zeroCal.TR = sum(a.TR for a in lZeroCal) / len(lZeroCal)
                
    f.close()
    
    return Cal0, Cal17, Cal34, zeroCal


########################################################################
#
########################################################################

"""
ReadFile(Directory, Filename)
print("CoP-Kg " + Filename)
StdData(lTestCoPKg, 2) 

newCoP = Build_CoP_from_RawData(lTestWii, zeroCal, Cal0, Cal17, Cal34)    
print("New CoP from RawData")
StdData(newCoP, 2)

#print("CoP")
#StdData(lTestCoP, 2)

print("CoG")
StdData(lTestCoG, 3)


""" 



