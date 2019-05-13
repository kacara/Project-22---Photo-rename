#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 18:08:39 2019

@author: caser
"""

#    1 import libraries
import os
#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from skimage import measure
from skimage import io
from skimage import transform
from skimage import color


# variable list
mule = []
m = []
dir_ = '/media/caser/Warehouse/Home2/Documents/02 Photo duplicate remove'
img_dict = {}


#   2 create filename list
m = os.listdir('./input')
df1 = pd.DataFrame({'Filename': m}).sort_values(by='Filename').reset_index(drop=True)
df1['Fullpath'] = './input/' + df1['Filename']
for i in range(df1.shape[0]):
    df1.loc[i,'Filesize'] = os.stat(df1.loc[i,'Fullpath']).st_size/1000


#   3 bulk read images
for i in range(df1.shape[0]):
    m = io.imread(df1.iloc[i,1])
    m = color.rgb2gray(m)
    m = transform.resize(m, (512, 512), mode='reflect')
    img_dict[i] = m

#   4 compare similarity
df2 = pd.DataFrame()
for i in range(df1.shape[0]):
    for k in range(df1.shape[0]):
        df2.loc[i,k] = measure.compare_nrmse(img_dict[i], img_dict[k], norm_type='Euclidean')


#   5 Mark similar images
for i in range(df1.shape[0]):
    df1.loc[i,'Similars'] = str(list(df2.columns[df2.loc[i,:] < 0.1]))


#   6 sort by filesize and filter the max by grouping
#   7 create kept and deleted tables
Kept = df1.sort_values(['Similars','Filesize'],ascending=False
                       ).groupby('Similars').head(1).sort_values('Filename')


Deleted = df1[~df1['Filename'].isin(Kept['Filename'])].sort_values('Filename')


#   8 Move files according to classification
Kept['Newpath'] = './output/' + Kept['Filename']
Deleted['Newpath'] = './duplicates/' + Deleted['Filename']

for i in range(Kept.shape[0]):
    os.rename(Kept.iloc[i,1], Kept.iloc[i,4])

for i in range(Deleted.shape[0]):
    os.rename(Deleted.iloc[i,1], Deleted.iloc[i,4])


#   9 write a report file
writer = pd.ExcelWriter('similars.xlsx')
df1.to_excel(writer, 'df1', float_format='%.f')
Kept.to_excel(writer, 'Kept', float_format='%.f')
Deleted.to_excel(writer, 'Deleted', float_format='%.f')
writer.save()

