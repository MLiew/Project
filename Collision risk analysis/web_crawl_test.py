'''
Author: Liew Ying Jia
Date: 15 Apr 2020
Description:    This is a web crawl module.
                Crawled website: www.celestrak.com
                This module will output the partially processed data into a .csv file
'''

import requests
from bs4 import BeautifulSoup
import csv
import os, sys
from os import path
from time import sleep
import pandas as pd
import numpy as np
import math

def get_homepage():
    # Get the homepage
    url = 'https://celestrak.com/NORAD/elements/'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",}

    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    # print(soup.prettify())
    return soup

def get_link(soup):
    link_body = soup.findAll("tr")

    # Extract a_href tag
    link_test = link_body[0].findAll("a", href = True)

    # Extract .txt name
    txt_link = []
    cnt_txt = 0

    for link in link_test:
        if cnt_txt == 0:
            txt_link.append(link.get('href'))
        if cnt_txt >=2:
            cnt_txt = 0
        else:
            cnt_txt += 1

    # Check if all string is .txt, if not, extract the index
    # 'not_txt' stores the index of not.txt element
    # Convert .txt link into urls
    str_txt = ".txt"
    not_txt = []
    txt_full_urls = []
    
    for link in txt_link:
        if str_txt in link:
            link =  'https://celestrak.com/NORAD/elements/%s' %link
        else:
            not_txt.append(txt_link.index(link))
            link = 'https://celestrak.com%s'%link
        txt_full_urls.append(link)
    
    # Replace filename from .php to .txt
    for num in not_txt:
        txt_link[num] = txt_link[num].replace(".php", str_txt)
        txt_link[num] = txt_link[num].replace("/satcat/", "") 
 
    return txt_full_urls, txt_link

def txt_webpage(link):
    # Send requests to internet server
    url = link
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",}

    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    src = response.text

    # Time interval for server to rest
    a = np.random.random_sample(1)
    sleep(a[0])
    print('sleep......')
    return src

def indv_txt_file_create(link, txt_link, filepath):
    folder = 'Tle_data_txt'
    # filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_test_file'
    newpath = filepath + '/' + folder

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    txt_filepath = newpath + '/' + txt_link
    if os.path.isfile(txt_filepath):
        pass
        # print ("%s exist, do nothing......" %txt_link)
    
    else:
        # print ("File not exist, creating file......")
        src = txt_webpage(link)
        fout = open(txt_filepath, "w", newline = '')
        fout.write(src)
        # print(src)
        fout.close()
        # print('%s is created'%txt_link)

def txt_file_create(txt_full_urls,txt_link, filepath):
    for url_link, txt in zip(txt_full_urls,txt_link):
        indv_txt_file_create(url_link, txt, filepath)

def read_file(txt_link, filepath):
    folder = 'Tle_data_txt'
    txt_filepath = filepath + '/' + folder + '/' + txt_link 
    fb = open(txt_filepath, 'r')
    f = fb.readlines()
    # print('Reading %s......' %txt_link)
    return f

def extract_txt(f, sat_name, txt_data):
    cnt = 0
    # Each data in f has 3 lines of information: name and two line elements  
    for line in f:
        # only need the first and third line
        if cnt == 0:
            sat_name.append(line.strip())
        elif cnt == 2:
            txt_data.append(line.split())
            # print(line.split())
        
        if cnt >= 2:
            cnt = 0
        else:
            cnt += 1
    # return sat_name, txt_data

def get_sat_data(txt_link, filepath):
    txt_data = []
    sat_name = []
    for txt in txt_link:
        f = read_file(txt, filepath)
        extract_txt(f, sat_name, txt_data)
    
    for data in txt_data:
        # delete the first two data
        if len(data) >= 8:
            del data[:2]
        
        # split the 6th element
        if len(data) == 6:
            n = 11
            dat = data[len(data)-1]
            chunks = [dat[data:data+n] for data in range(0, len(dat), n)]
            # print(chunks)
            del data[5]
            for k in range(2):
                data.insert(5+k, chunks[k])
            # print('chunks function called')
            
        # convert eccentricity into decimal points
        eccen = int(data[2])/10000000
        # print(eccen)
        data[2] = '%s' %eccen
    
    # zip the name column and the data columns
    for txt, sat in zip(txt_data, sat_name):
        # insert the name column
        txt.insert(0, sat)
    # print(txt_data)
    # print("Get Satellite Function done!!!")    

    # check the duplicated elements and remove it
    test_test = txt_data
    remove_dup_data = [] # name of the data

    for data in test_test:
        if data not in remove_dup_data:
            remove_dup_data.append(data)
    
    # print(remove_dup_data[1])
    return remove_dup_data

def SemiAxis(period):
    miu = 3.986005*1e+14
    Period = float(period)
    ans = pow(pow((Period/(2*math.pi)), 2)*miu, 1/3)
    return ans

def convert_smaxis(remove_dup_data):
    Period = []
    SAxis = []

    for i in range(len(remove_dup_data)):
        Period.append(remove_dup_data[i][6])
        Period[i] = (24*60*60)/float(Period[i])
        flt_period = float(Period[i])
        
        # Call Semi Axis function
        SAxis.append(SemiAxis(flt_period))
    return Period, SAxis 

def tle_data_csv(remove_dup_data, Period, SAxis, filepath):
    # # Calling DataFrame constructor after zipping both lists, with columns specified 
    df = pd.DataFrame(remove_dup_data, columns = ['Name', 'Inclination', 'RAAN', 'Eccentricity', 
                                    'Argument of Perigee','Mean Anomaly', 'Mean Motion',
                                    'Revolution Num'])
    df['Period(s)'] = Period
    df['Semi Major Axis(m)'] = SAxis
    
    folder = 'csv_file'
    newpath = filepath + '/' + folder

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    filename = 'TLE_data.csv'
    csv_filepath = newpath + '/' + filename
    
    df.to_csv (r'%s'%csv_filepath, index = False, header=True)
    return csv_filepath

def main_web_crawl(filepath):
    # print(sys.getrecursionlimit())
    soup = get_homepage()
    txt_full_urls, txt_link = get_link(soup)
    # print("Get link module called")
    txt_file_create(txt_full_urls,txt_link, filepath)
    # print("tle data text files created...")
    remove_dup_data = get_sat_data(txt_link, filepath)
    Period, SAxis = convert_smaxis(remove_dup_data)
    csv_filepath = tle_data_csv(remove_dup_data, Period, SAxis, filepath)
    return csv_filepath
    
if __name__ == "__main__":
    filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_test_file'
    main_web_crawl(filepath)