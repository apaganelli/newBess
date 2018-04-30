# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 21:10:18 2018

@author: anton
"""

class RawLoadCell:
    def __init__(self, BottomLeft, BottomRight, TopLeft, TopRight, Time):
        self.BL = BottomLeft
        self.BR = BottomRight
        self.TL = TopLeft
        self.TR = TopRight
        self.Time = Time
        # self.Total = BottomLeft + BottomRight + TopLeft + TopRight

class Raw2DTimePoint:
    def __init__(self, Time, X, Y):
        self.Time = Time
        self.X = X
        self.Y = Y

class Raw3DTimePoint:
    def __init__(self, Time, X, Y, Z):
        self.Time = Time
        self.X = X        
        self.Y = Y
        self.Z = Z

class BodyFrame:
    def __init__(self, Time):
        self.Time = Time
        self.Joints = []

class JointPosition:
    def __init__(self, Id, Status, X, Y, Z):
        self.Id= Id
        self.Status = Status
        self.X = X
        self.Y = Y
        self.Z = Z

class Eyes:
    def __init__(self, Time, Status):
        self.Time = Time
        self.Status = Status

class StdResults2D:
    def __init__(self, MinX, MaxX, MeanX, StdDevX, RMSX, normalX,
                 MinY, MaxY, MeanY, StdDevY, RMSY, normalY,
                 total, peakVel, avgVel):
        self.MinX = MinX
        self.MaxX = MaxX
        self.AmpX = MaxX - MinX
        self.MeanX = MeanX
        self.StdDevX = StdDevX
        self.RMSX = RMSX
        self.NormalX = normalX
        self.MinY = MinY
        self.MaxY = MaxY
        self.AmpY = MaxY - MinY
        self.MeanY = MeanY
        self.StdDevY = StdDevY
        self.RMSY = RMSY
        self.NormalY = normalY        
        self.TotalPathLen = total
        self.PeakVel = peakVel
        self.AvgVel = avgVel


class StdResults3D:
    def __init__(self, MinX, MaxX, MeanX, StdDevX, RMSX, normalX,
                 MinY, MaxY, MeanY, StdDevY, RMSY, normalY,
                 MinZ, MaxZ, MeanZ, StdDevZ, RMSZ, normalZ,
                 total, peakVel, avgVel):
        self.MinX = MinX
        self.MaxX = MaxX
        self.AmpX = MaxX - MinX
        self.MeanX = MeanX
        self.StdDevX = StdDevX
        self.RMSX = RMSX
        self.NormalX = normalX
        self.MinY = MinY
        self.MaxY = MaxY
        self.AmpY = MaxY - MinY
        self.MeanY = MeanY
        self.StdDevY = StdDevY
        self.RMSY = RMSY
        self.NormalY = normalY   
        self.MinZ = MinZ
        self.MaxZ = MaxZ
        self.AmpZ = MaxZ - MinZ
        self.MeanZ = MeanZ
        self.StdDevZ = StdDevZ
        self.RMSZ = RMSZ
        self.NormalZ = normalZ        
        self.TotalPathLen = total
        self.PeakVel = peakVel
        self.AvgVel = avgVel



