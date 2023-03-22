# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 00:36:46 2023

@author: simps
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from scipy import signal
import wget
from retrying import retry
import os
# 解析链接
def parse(url,urllist,namelist):
    root = 'https://pds-geosciences.wustl.edu'
    #请求发送网页
    html=requests.get(url)
    #网页内容转化
    html = html.text
    #标签格式排列
    soup = BeautifulSoup(html,'lxml')
    # 找到a标签
    data = soup.find_all('a')
    for i in data:
        name = i.text
        if 'sol' in name:
            parse(root+i.get('href'),urllist,namelist)
        if 'rrs' in name and '.csv' in name:
            urllist.append(root+i.get('href'))
            namelist.append(name)
@retry(stop_max_attempt_number=10, wait_random_min=10000, wait_random_max=20000)
def getCSV(url,path):
    
    wget.download(url,path)
 

def CheckCSV(name,path):
    for file in os.listdir(path):
        if name == file:
            return bool(0)
    return bool(1)

def CSVtoData(url):
    df = pd.read_csv(url,header=1,engine="python")
    for n,i in enumerate(df.iloc[:, 0]):
        if 'REGION_1' in i:
            s1 = n
        if 'REGION_2' in i:
            s2 = n
        if 'REGION_3' in i:
            s3 = n
    Df1=df.iloc[s1+2:s2,].T
    Df2=df.iloc[s2+2:s3,].T
    return Df1,Df2

def findpeaks(array,name):
    for col in array.T:
        col=list(col)
        col=list(map(float,col))
        a = col[236:247]
        b = max(a)
        peaks,_ = signal.find_peaks(col[181:203], height=2*float(b), distance=10)
        if len(peaks)!=0:
            print(peaks)
            print(name)

if __name__ == '__main__':
    # 给定一个初始的url

    url='https://pds-geosciences.wustl.edu/m2020/urn-nasa-pds-mars2020_sherloc/data_processed/'
    path='E:\RECORD\Sherloc'
    # 解析该url
    urllist = []
    namelist = []
    parse(url,urllist,namelist)
    with open('urllist.txt','w') as f:
        f.writelines(urllist)
        f.close()
    for n,i in enumerate(urllist):
        if CheckCSV(namelist[n],path):
            getCSV(i,path)
        print(" %d"%(n)+"/305")
#这一模式下不需要下载CSV文件直接进行处理
    # for i,key in enumerate(urllist): 
    #     df1,df2=CSVtoData(key)
    #     findpeaks(df1.values,namelist[i])
    #     findpeaks(df2.values,namelist[i])
#已经下载完CSV后进行读取
    for file in os.listdir(path):
        fpath = os.path.join(path, file)
        df1,df2 = CSVtoData(fpath)
        findpeaks(df1.values,namelist[i])
        
    
