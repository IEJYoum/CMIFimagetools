# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 16:21:55 2021

@author: youm
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image   #skimage
import time
import copy


Image.MAX_IMAGE_PIXELS = 992571125

#folder = "C:/Users/youm/Desktop/Registration/210405/"  #

startTime = time.time()
#find/implement ram tracker

keyRound = "1"
keyChannel = "1"
#write wrapper to take filename parsing



 
            
 
def followPath(A,path,zLevel):
    for step in path:
        if step == 1:
            for i in range(zLevel):
                A = moveUp(A)
        if step == 2:
            for i in range(zLevel):
                A = moveDown(A)           
        if step == 3:
            for i in range(zLevel):
                A = moveLeft(A)        
        if step == 4:
            for i in range(zLevel):
                A = moveRight(A)
    return(A)
    

def getMap(key,array):
    #gets paths, doesn't move anything
    A = array
    path = []
    bestInd = 5
    while bestInd != 0:
        wiggles = [A,moveUp(A),moveDown(A),moveLeft(A),moveRight(A)]  #0stationary,1up,2down,3left,4right          
        scores = []
        for w in wiggles:
            scores.append(score(key,w)) #[unmoved score,()]        
        bestInd = scores.index(min(scores))
        A = wiggles[bestInd]
        path.append(bestInd)
    return(path)


def score(A,B):
    cost = np.sum(np.square(np.subtract(A,B)))
    return(cost)
       
 
def moveUp(A): 
    shape = A.shape
    upA = A[1:,:]
    upA = np.append(upA,[np.ones(shape[1])],axis=0)   
    return(upA)
def moveDown(A):
    shape = A.shape
    downA = A[:-1,:]
    downA = np.append([np.ones(shape[1])],downA,axis=0)    
    return(downA)
def moveLeft(A): 
    shape = A.shape
    leftA = A[:,1:]
    leftA = np.append(leftA,np.ones((shape[0],1)),axis=1)    
    return(leftA)
def moveRight(A):  
    shape = A.shape
    rightA = A[:,:-1]
    rightA = np.append(np.ones((shape[0],1)),rightA,axis=1)
    return(rightA)


def zoom(array,n):#chops array into nxn pixel chunks
    yCursor = 0
    shape = array.shape
    newA = np.zeros((int(shape[0]/n),int(shape[1]/n)))
    while yCursor + n <= shape[0]:
        xCursor = 0
        while xCursor + n <= shape[1]:
            chunk = array[yCursor:yCursor+n,xCursor:xCursor+n]
            newA[int(yCursor/n),int(xCursor/n)] = np.mean(chunk)
            xCursor += n
        yCursor += n
    return(newA)

def load(folder,fileName):
    print("loading:",folder,fileName)
    f = Image.open(folder+fileName)
    array = np.array(f)
    f.close()
    return(array)


def read(folder,keyChannel="_c1_",keyRound="R1_",scene="cene-1"): #use pandas, make pandas column and rounds column and scenes column
                                                    #will take string inputs for master(key) and moving 
    keyChannel = int(keyChannel[2])
    keyRound = int(keyRound[1])
    scene = int(scene[-1])    
    maxRounds = 20 # > range to search
    maxColors = 10
    fileNames = np.zeros((maxRounds+1,maxColors+1),dtype = object) 
    for file in os.listdir(folder):
        for i in range(maxRounds+1): 
            for j in range(maxColors+1): 
                if "R"+str(i)+"_" in file and "c"+str(j)+"_" in file and "cene-"+str(scene)+"_" in file and "registered-" not in file:
                    fileNames[i,j] = file 
    fileNames = np.append(np.append(fileNames[keyRound:keyRound+1,:],fileNames[:keyRound,:],axis=0),fileNames[keyRound+1:,:],axis=0)
    fileNames = np.append(np.append(fileNames[:,keyChannel:keyChannel+1],fileNames[:,:keyChannel],axis=1),fileNames[:,keyChannel+1:],axis=1)
    
    return(fileNames)
    
            

def cost_function_registration(inputPath, outputPath, sceneStr = "cene-1", masterChannel = "_c1_", masterRound = "R1_"): #inputs: filepath, scene pattern, rounds pattern, channel pattern, outputpath
    fileNames = read(inputPath,keyChannel=masterChannel,keyRound=masterRound,scene=sceneStr)  #rename read and main (to be more unique) 
    try:
        key = load(inputPath,fileNames[0,0]) 
    except:
        print("error loading key file, check keyRound and keyChannel")
        return()
    for i in range(1,fileNames.shape[0]):
        name = fileNames[i,0]
        if name == 0:
            continue
        zLevel = 500 #Make starting zLevel a fraction of the whole image
        movingA = load(inputPath,name)
        paths = []
        levels = []
        while zLevel > 2:
            smallKey = zoom(key,zLevel) 
            smallA = zoom(movingA,zLevel)
            path = getMap(smallKey,smallA)
            paths.append(path)
            levels.append(zLevel)
            if len(path)>1:
                movingA = followPath(movingA,path,zLevel)
            zLevel = int(zLevel/1.5)
        path = getMap(key,movingA)
        movingA = followPath(movingA,path,1)
        paths.append(path)
        levels.append(1)
        file = Image.fromarray(movingA)
        file.save(outputPath+"registered1-"+name+'.tif')
        file.close  
        
        for j in range(1,fileNames.shape[1]):
            if fileNames[i,j] != 0:
                try:
                    followName = fileNames[i,j]
                    followingA = load(inputPath,followName)
                    for k in range(len(paths)):
                        followingA = followPath(followingA,paths[k],levels[k])
                    file = Image.fromarray(followingA)
                    file.save(outputPath+"registered1-"+followName+'.tif')
                    file.close  
                except:
                        print("error processing",fileNames[i,j])

if __name__ == '__main__':
    cost_function_registration(inputPath="C:/Users/youm/Desktop/Registration/210405/", outputPath="C:/Users/youm/Desktop/Registration/210405/", sceneStr = "cene-1", masterChannel = "_c1_", masterRound = "R1_")
    
    
    
    
   
    
    
    
    
    
#upload to github -- pick name, git repository
#to make pip-installible make sure name not taken

#other:
#fix filenames and make new PNG
    
    
    
    
    
    
    
    