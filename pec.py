#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:37:50 2017

@author: dyan
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def read_par(file):

    with open(file, 'r') as fin:
        data = list()
        for line in fin:
            if not line.startswith('Definition=Segment'):
                continue
            else:
                header = line.split(", ")[0:-1]
                while True:
                    s = fin.readline()
                    if s.startswith('</Segment1>'):
                        break
                    else:
                        data.append(s)
    #                    print(s)
                break
    
    df = pd.DataFrame([sub.split(",") for sub in data], columns = header)
    rdata = df[['E(V)', 'I(A)']].astype(float).round({'E(V)': 2})
    
    return rdata

def rhe(df, delta_E):
    
    df['E(V)'] += delta_E
    df['I(A)'] /= 0.18
    new = df.groupby('E(V)').mean().reset_index()
    
    return new
    
# change to the file directory
os.chdir('/Users/dyan/Desktop')

# read E/I columns from a *.par data file as a table(pandas dataframe)
filename = 't.par'
data = read_par(filename)

# convert to RHE voltages
new = rhe(data, 1)

# plot averaged photocurrents
new.plot(x = 'E(V)', y = 'I(A)')
plt.show()

# save data to *.csv
new.to_csv('%s.csv' % filename[0:-4], index = False)