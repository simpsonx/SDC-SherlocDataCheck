# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 01:49:36 2023

@author: simps
"""
import os
import csv
import pandas as pd
from scipy import signal

def CSVtoData(url):
    global s1, s2, s3
    df = pd.read_csv(url, header=1, engine="python")
    for n, i in enumerate(df.iloc[:, 0]):
        if 'REGION_1' in i:
            s1 = n
        if 'REGION_2' in i:
            s2 = n
        if 'REGION_3' in i:
            s3 = n
    Df1 = df.iloc[s1 + 2:s2, ].T
    Df2 = df.iloc[s2 + 2:s3, ].T
    return Df1, Df2

def findpeaks(array):
    n = 0
    m = 0
    for col in array.T:
        col = list(col)
        col = list(map(float, col))
        a = col[236:247]
        b = max(a)
        peaks, _ = signal.find_peaks(col[181:203], height=2 * float(b), distance=10)
        if any(9 <= i <= 14 for i in peaks):
            n = n + 1
        m = m + 1
    return n, m


def writemark(my_list):
    with open("CSVmark.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(my_list)
        f.close()
        
if __name__ == '__main__':
    path = 'E:\RECORD\Sherloc'
    writemark(['file', 'region1', 'region2', 'count', 'r1mark', 'r2mark'])
    for file in os.listdir(path):
        fpath = os.path.join(path, file)
        df1, df2 = CSVtoData(fpath)
        p1, l1 = findpeaks(df1.values)
        p2, l2 = findpeaks(df2.values)
        writemark([file, p1, p2, l1, p1/l1, p2/l2])