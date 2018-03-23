# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:44:10 2018

@author: gmallya
"""

import numpy as np
import pandas as pd
import time
from datetime import timedelta, date
import re
from selenium import webdriver
from bs4 import BeautifulSoup

##### User defined function to get a list of dates between two dates #####
def daterange(start_date, end_date): #start_date = year(YYYY, MM, DD)
    for dt_frac in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(dt_frac)
##########################################################################
        
Y1 = 2018
M1 = 01
D1 = 01
Y2 = 2018
M2 = 01
D2 = 31

driver = webdriver.Chrome('C:/Users/gmallya/Downloads/chromedriver')
driver.get('https://www.wunderground.com/history/airport/KLAF/2018/3/22/DailyHistory.html?req_city=West+Lafayette&req_state=IN&req_statename=Indiana&reqdb.zip=47906&reqdb.magic=1&reqdb.wmo=99999')


start_dt = date(Y1, M1, D1)
end_dt = date(Y2, M2, D2)
dt_list = []
for dt in daterange(start_dt, end_dt):
    dt_list.append(dt.strftime("%m/%d/%Y"))
    
Month = 'February'
Day = '2'
Year = '2018'
month = driver.find_element_by_class_name('month')
month.send_keys(Month)
day = driver.find_element_by_class_name('day')
day.send_keys(Day)
year = driver.find_element_by_class_name('year')
year.send_keys(Year)
year.submit()

html = driver.page_source
soup = BeautifulSoup(html,"lxml")
table = soup.findAll("div",id="observations_details")
ind = 0
with open('data.csv', 'w') as data:
    for row in table[0].find_all('tr'):
        item_ind = 0
        if ind == 0: # Read header
            for header in row.find_all('th'):
                if item_ind > 0:
                    data.write('; ')
                data.write(header.text.encode('utf-8').strip())
                item_ind = item_ind + 1
            data.write('\n')
        else: 
            for wdata in row.find_all('td'):
                if item_ind > 0:
                    data.write('; ')
                data.write(wdata.text.encode('utf-8').strip())
                item_ind = item_ind + 1
            data.write('\n')
        ind = ind + 1
        
driver.quit()