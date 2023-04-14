# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 01:38:52 2023

@author: simps
"""

import csv
import os.path

import pandas as pd
import matplotlib.pyplot as plt


def find_namelist():
    max_value = 2
    namelist = []
    with open('CSVmark.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[6] == str(max_value):
                namelist.append(row[0])
    return namelist


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
    Df1 = df.iloc[s1 + 2:s2, ]
    return Df1


def get_wavenumber():
    with open('wavenumber.txt', 'r') as f:
        lines = f.readlines()
        wavenumber = [float(line.split()[0]) for line in lines]
        num = [i for i in range(len(wavenumber)) if wavenumber[i] > 500 and wavenumber[i] < 3000]
    return wavenumber, num


def draw_csv(name):
    # name = 'ss__0181_0683039785_555rrs__0070000srlc15090bz08zpzj03.csv'
    path_i = os.path.join(path, name)
    # temp_path = 'E:\RECORD\Sherloc\ss__0181_0683039785_555rrs__0070000srlc15090bz08zpzj03.csv'
    df = csv_to_data(path_i)
    # Select a row of data
    for index1, row in df.iterrows():
        # Plot the row as a line
        y = row.values
        y = [y[i] for i in num]
        y = list(map(float, y))

        fig, ax = plt.subplots(figsize=(19.20, 10.80))
        ax.plot(wavenumber, y, linewidth=0.5)
        ax.set_title(name)
        ax.set_xlabel('wavenumber')
        ax.set_ylabel('counts')
        plt.savefig('%s.png' % (name[:-4]), dpi=300)
    plt.show()


if __name__ == '__main__':
    path = 'E:\RECORD\Sherloc'
    namelist = find_namelist()
    wavenumber, num = get_wavenumber()
    wavenumber = [wavenumber[i] for i in num]
    for name in namelist:
        draw_csv(name)
    # for i in namelist:
    #
