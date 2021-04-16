# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 13:29:34 2021

@author: youm
"""

#biotransistor

import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import copy
import scanpy as sc
import anndata
import math
import seaborn as sns
import phenograph
from scipy import sparse
from sklearn.metrics import adjusted_rand_score
import re

manualThresh = {'53BP1_nuclei': 2750,'CAV1_perinuc5': 2000, 'CC3_perinuc5': 2250,'CD20_perinuc5': 2000, 'CD31_perinuc5': 2000, 'CD3_perinuc5': 1500, 'CD44_perinuc5': 1500, 'CD45_perinuc5': 1000, 'CD4_perinuc5': 2000, 'CD68_perinuc5': 3500, 'CD8_perinuc5': 5000,
                'CK14_perinuc5': 1000, 'CK17_perinuc5': 1500, 'CK19_perinuc5': 2000,'CSF1R_perinuc5': 3000, 'ColIV_perinuc5': 4000, 'ColI_perinuc5': 6000, 'CoxIV_perinuc5': 1500,
                'EGFR_perinuc5': 2500,'FoxP3_nuclei': 3000,'GRNZB_nuclei': 1500,'H3K27_nuclei': 1250, 'H3K4_nuclei': 2250,
                'Ki67_nuclei': 1500,'LamAC_nuclei': 1250,'MSH6_nuclei': 1500, 'MUC1_perinuc5': 1750,'PCNA_nuclei': 2000, 'PD1_perinuc5': 3250, 'PDL1_perinuc5': 3000,'RAD51_nuclei': 2500,'SYP_perinuc5': 2000,'TFF1_perinuc5': 1750,'VIM_perinuc5': 1000,'aSMA_perinuc5': 2000,'cPARP_nuclei': 1500,'gH2AX_nuclei': 1500,'p63_nuclei': 1750, 'pAKT_perinuc5': 2000, 'pERK_nuclei': 2600, 'pHH3_nuclei': 2000, 'pS6RP_perinuc5': 2500, }

#, 'Ecad_perinuc5': 2000, , 'pERK_perinuc5': 2600 missing from csv files

COLUMNS = []
for val in manualThresh:
    COLUMNS.append(val)

FOLDER = "C:/Users/youm/Desktop/210316 data/"
NAMES = [["394","406","388"],["BrightMeanIntensity","CentroidXY","FilteredMeanIntensity_DAPI"]] 
#must have at least 1 string from each list


a = "ding"


def main():
    framesT,filenames = getDataframes(NAMES) #loads data 
    DF = merge(framesT,filenames)
    DF.rename({'CK8_perinuc5': 'VIM_perinuc5'}, axis=1, inplace=True)
    
    #DF = DF.loc[:,COLUMNS] for only manualThresh values
    #return()
    DF.to_csv(FOLDER+"394_406_388_allCols.csv")
    #np.savetxt(FOLDER+"npcombined_394_and_406_2.csv",DF.values)


def merge(framesT,filenames):
    df = framesT[0]
    print("starting with",filenames[0])
    unmerged = []
    unnames = []
    for i in range(1,len(filenames)):
        print(filenames[i])
        newFrame = framesT[i]
        indInter = sorted(set(df.index).intersection(newFrame.index))
        colInter = sorted(set(df.columns).intersection(newFrame.columns))
        #indOuter = set(df.index).union(newFrame.index)
        #colOuter = set(df.columns).union(newFrame.columns)
        indFrac = len(list(indInter))/len(newFrame.index)
        colFrac = len(list(colInter))/len(newFrame.columns)
        print("mutual index intersections", indFrac)
        print("mutual column intersections", colFrac)
        if indFrac > colFrac: #writes intersect inds and union cols
            df = df.loc[indInter,:]
            newFrame = newFrame.loc[indInter,:] #checks that the cols in newFrame aren't already in df
            for repeatCol in colInter:
                newFrame = newFrame.drop(repeatCol,axis=1)
            df = pd.DataFrame(data = np.append(df.values,newFrame.values,axis=1), 
                              index = indInter, 
                              columns = np.append(df.columns.values,newFrame.columns.values))
            #df = df.loc[:,colOuter] #redundant?
        else:
            unmerged.append(newFrame)
            unnames.append(filenames[i])
    if len(unmerged) > 0:
        df2 = merge(unmerged,unnames)
        colInter = sorted(set(df.columns).intersection(df2.columns))
        df = df.loc[:,colInter]
        df2 = df2.loc[:,colInter]
        df = pd.DataFrame(data = np.append(df.values, df2.values, axis=0),
                          index = np.append(df.index.values, df2.index.values),
                          columns = df.columns)
    print(df.shape)
    #df = df.loc[sorted(set(df.index)),sorted(set(df.columns))]
    return(df)
      
    
    
    
def getDataframes(names):
    #search function to find files based on NAMES list
    framesT = []
    filenames = []
    shape = np.array(names,dtype=object).shape   
    for file in os.listdir(FOLDER):
        scores = np.zeros(shape[0])
        i = 0
        for lis in names: 
            for el in lis:
                if el in file:
                    scores[i] = 1
                    #print(el,file)
            i += 1
                    
        if np.sum(scores) == shape[0]:
            framesT.append(pd.read_csv(FOLDER+file,index_col=0))
            filenames.append(file)
    #print(scores)
    print(filenames)
    return(framesT,filenames)
                
            
        

    
main()