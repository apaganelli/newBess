# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 21:06:36 2018

@author: anton
"""

from Classes import Raw2DTimePoint

# RawData is a list of the type 
def Build_CoP_from_RawData(RawData, zeroCal, Cal0, Cal17, Cal34 ):
    
    lCoP = []
        
    for item in RawData:        
        
        item.BL -= zeroCal.BL
        item.BR -= zeroCal.BR
        item.TL -= zeroCal.TL
        item.TR -= zeroCal.TR
        
        if item.BL <= Cal17.BL:
            item.BL = (17 * item.BL) / (Cal17.BL - Cal0.BL)
        else:
            item.BL = (34 * item.BL) / (Cal34.BL - Cal0.BL)
        
        if item.BR <= Cal17.BR:
            item.BR = (17 * item.BR) / (Cal17.BR - Cal0.BR)
        else:
            item.BR = (34 * item.BR) / (Cal34.BR - Cal0.BR)
        
        if item.TL <= Cal17.TL:
            item.TL = (17 * item.TL) / (Cal17.TL - Cal0.TL)
        else:
            item.TL = (34 * item.TL) / (Cal34.TL - Cal0.TL)
        
        if item.TR <= Cal17.TR:
            item.TR = (17 * item.TR) / (Cal17.TR - Cal0.TR)
        else:
            item.TR = (34 * item.TR) / (Cal34.TR - Cal0.TR)
                                
        #print("%2.2f   %2.2f   %2.2f   %2.2f" %(item.BL, item.BR, item.TL, item.TR))
                    
        x = (433/2) * (((item.TR + item.BR) - (item.TL + item.BL)) / 
             (item.BL + item.BR + item.TL + item.TR))
        
        y = (238/2) * (((item.TR + item.TL) - (item.BR + item.BL)) / 
             (item.BL + item.BR + item.TL + item.TR))
      
        CoP = Raw2DTimePoint(item.Time, x, y)
        lCoP.append(CoP)
        
    return lCoP

