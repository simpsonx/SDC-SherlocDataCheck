# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 01:49:36 2023

@author: simps
"""
import os
import csv
import pandas as pd
from scipy import signal


# noinspection PyGlobalUndefined
def csv_to_data(url):
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
    return Df1


def find_peaks(array):
    peak1n = 0
    peak2n = 0
    m = 0
    for col in array.T:
        col = list(col)
        col = list(map(float, col))
        a = col[236:247]
        b = max(a)
        peaks, _ = signal.find_peaks(col[181:203], height=2 * float(b), distance=10)
        if any(8 <= i <= 12 for i in peaks):
            peak1n = peak1n + 1
            peaks2, _ = signal.find_peaks(col[151:182], height=2 * float(b), distance=10)
            if any(11 <= i <= 19 for i in peaks2):
                peak2n = peak2n + 1
        m = m + 1
    return peak1n, peak2n, m


def write_mark(my_list):
    with open("CSVmark.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(my_list)
        f.close()


if __name__ == '__main__':
    path = 'E:\RECORD\Sherloc'
    write_mark(['file', 'region1p1', 'region1p2', 'count', 'r1rank1', 'r1rank2', 'SUM'])
    for file in os.listdir(path):
        fpath = os.path.join(path, file)
        df1 = csv_to_data(fpath)
        p1, p2, l1, = find_peaks(df1.values)
        write_mark([file, p1, p2, l1, p1 / l1, p2 / l1, p1 / l1 + p2 / l1])
