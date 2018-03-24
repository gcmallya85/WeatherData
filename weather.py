# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:44:10 2018

@author: gmallya
"""

from datetime import timedelta, date
from selenium import webdriver
from bs4 import BeautifulSoup

############## Date range provided by the user ##########################        
Y1 = 2018
M1 = 01
D1 = 01
Y2 = 2018
M2 = 01
D2 = 05
#########################################################################


##### User defined function to get a list of dates between two dates #####
def daterange(start_date, end_date): #start_date = year(YYYY, MM, DD)
    for dt_frac in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(dt_frac)
##########################################################################

driver = webdriver.Chrome('C:/Users/gmallya/Downloads/chromedriver')
#driver.get('https://www.wunderground.com/history/airport/KLAF/2018/3/22/DailyHistory.html?req_city=West+Lafayette&req_state=IN&req_statename=Indiana&reqdb.zip=47906&reqdb.magic=1&reqdb.wmo=99999')


start_dt = date(Y1, M1, D1)
end_dt = date(Y2, M2, D2)

dt_list = []
for dt in daterange(start_dt, end_dt):
    dt_list.append(dt.strftime("%Y/%m/%d"))

month_name = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May',
              '06':'June', '07':'July', '08':'August', '09':'September', '10':'October',
              '11':'November', '12':'December'}

ind = 0
with open('data.csv', 'w') as data:
    dt_ind = 0
    for dts in dt_list:
        if dt_ind == 0:
            driver.get('https://www.wunderground.com/history/airport/KLAF/'+ dts + '/DailyHistory.html?req_city=West+Lafayette&req_state=IN&req_statename=Indiana&reqdb.zip=47906&reqdb.magic=1&reqdb.wmo=99999')
        else:
            Month = month_name[dts[5:7]]
            if int(dts[8:])<10:
                Day = dts[9:]
            else:
                Day = dts[8:]
            Year = dts[0:4]
            month = driver.find_element_by_class_name('month')
            month.send_keys(Month)
            day = driver.find_element_by_class_name('day')
            day.send_keys(Day)
            year = driver.find_element_by_class_name('year')
            year.send_keys(Year)
            year.submit()
        
        dt_ind = dt_ind + 1
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        table = soup.findAll("div",id="observations_details")
        for row in table[0].find_all('tr'):
            item_ind = -1
            if ind == 0: # Read header
                for header in row.find_all('th'):
                    if item_ind == -1:
                        data.write('Date; ') # Label the date column
                    elif item_ind > 0:
                        data.write('; ')
                    data.write(header.text.encode('utf-8').strip()) # Label the data columns by reading the header information for the columns
                    item_ind = item_ind + 1
                data.write('\n')
            else:
                found_td = 0
                for wdata in row.find_all('td'):
                    if item_ind == -1: # Write the date
                        data.write(dts +'; ')
                        found_td = 1
                    if item_ind > 0:
                        data.write('; ')
                    data.write(wdata.text.encode('utf-8').strip()) # Write the data stored in each row of the table
                    item_ind = item_ind + 1
                if found_td == 1: # Takes care of extra new line character when writing data for second date and so on
                    data.write('\n')
            ind = ind + 1
        
driver.quit()