# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 13:24:39 2021

@author: youm
"""

#for cropping will have the list of coords and type [0,0,0,0,"xyxy"] [0,0,0,0,"xywh"] None, default none
#input and output path

import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = 992571125

def crop(inPath,outPath,coords):
    array = load(inPath)
    if type(coords) == list:
        array = remove(array,coords)
    file = Image.fromarray(array)
    file.save(outPath)
    file.close()
    

def remove(array,coords):
    if coords[-1] == "xyxy":
        array = array[coords[1]:coords[3],coords[0]:coords[2]]
    elif coords[-1] == "xywh":
        array = array[coords[1]:coords[1]+coords[3],coords[0]:coords[0]+coords[2]]
    else:
        print("[0,0,0,0,'str'] str not understood, use 'xyxy' or 'xywh'")
    return(array)
    
    
    
def load(inPath):    
    print("loading:",inPath)
    f = Image.open(inPath)
    array = np.array(f)
    f.close()
    return(array)



if __name__ == '__main__':
    inPath = "C:/Users/youm/Desktop/Registration/test2/Registered-R0_R0c2.R0c3.R0c4.R0c5_SDA845-5-Scene-010_c1_ORG.tif"
    outPath = "C:/Users/youm/Desktop/Registration/test2/Cropped-R0_R0c2.R0c3.R0c4.R0c5_SDA845-5-Scene-010_c1_ORG.tif"
    coords = [3917,3152,7226,7991,'xywh']
    crop(inPath,outPath,coords) 
    
    
    
    
    