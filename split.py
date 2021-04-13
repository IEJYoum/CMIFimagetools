# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 13:24:39 2021

@author: youm
"""

#for cropping will have the list of coords and type [0,0,0,0,"xyxy"] [0,0,0,0,"xywh"] None, default none
#input and output path

import numpy as np
#import matplotlib.pyplot as plt
#import os
from PIL import Image
import math

Image.MAX_IMAGE_PIXELS = 992571125

MAXOUTPUTDIM = 5000 #by 20000, 100 by 100

def main(inPath,outPath,coords):
    array = load(inPath)
    if type(coords) == list:
        array = crop(array,coords)
        scenes = split(array)
    shape = scenes.shape
    print("split into _ x _:",shape)
    for i in range(shape[0]):
        for j in range(shape[1]): 
            scene = scenes[j,i]
            print(scene.shape)
            file = Image.fromarray(scene)
            file.save(outPath+str(i)+str(j)+".tif")
            file.close()
            



def split(array):
    shape = array.shape
    W = math.ceil(shape[1]/MAXOUTPUTDIM)
    H = math.ceil(shape[0]/MAXOUTPUTDIM)
    thinAs = []
    for i in range(W):
        startpoint = round(i/W*shape[1])
        endpoint =  round((i+1)/W*shape[1])
        thinAs.append(array[:,startpoint:endpoint])
    smallAs = np.zeros((H,W),dtype=object)
    for i in range(len(thinAs)):
        A = thinAs[i]
        for j in range(H):
            startpoint = round(j/H*shape[0])
            endpoint =  round((j+1)/H*shape[0])
            smallAs[j,i] = A[startpoint:endpoint,:]
    return(smallAs)
        
        
        
    
    

        


def crop(array,coords):
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
    coords = [100,100,12000,12000,'xywh']
    main(inPath,outPath,coords) 
    
    
    
    
    