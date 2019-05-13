#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 19:59:13 2018

@author: caser
"""
#   1 import modules
#import numpy as np
import pandas as pd
import os
import datetime


#   2 variable list
# define pathname
path = "/media/caser/Warehouse/Home2/Documents/01 Photo rename/input1/"
# create a df for listing
df1 = pd.DataFrame(columns=['Dirpath', 'Old Filename', 'Modified'])

#   3 bulk read directory, file names and write into df1
for dirpath, dirnames, filenames in os.walk(path):
    for i in filenames:
        m = os.path.getmtime(str(dirpath + i))
        m = datetime.datetime.fromtimestamp(int(m)).strftime('%Y%m%d%H%M%S')
        m_ = pd.DataFrame({'Dirpath': [dirpath],'Old Filename':[i],'Modified':[m]})
        df1 = df1.append(m_, ignore_index=1)


#   4 create new filename
df1 = df1.sort_values(by=['Modified']).reset_index(drop=True)
df1['Newname'] = df1['Modified'].str[0:4] + '-' + df1['Modified'].str[4:6] + '-' + df1['Modified'].str[6:8] + '-IMG-' + df1.index.values.astype(str) + '' + df1['Old Filename'].str[-4:].str.lower()


#   5 apply renaming per file
for i in range(df1.shape[0]):
    old = os.path.join(df1.loc[i,'Dirpath'], df1.loc[i,'Old Filename'])
    new = os.path.join(df1.loc[i,'Dirpath'], df1.loc[i,'Newname'])
    os.rename(old, new)



