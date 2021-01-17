# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 12:57:28 2018

@author: George
"""

###This script written for Nathan to automate querying the Blaine County search engine to discover which land parcels have structures built on them 

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import pandas as pd
from tqdm import tqdm


df=pd.read_csv(r'C:\Users\George\Desktop\Nathan\Parcels_BlaineCo_PrivateOnly_20180420.txt', sep=',')
#df.values

savePath = (r'C:\Users\George\Desktop\Nathan\residences_BlaineCo_Result.csv')

driver = webdriver.Chrome(r'C:\Program Files\chromedriver.exe')  # Optional argument, if not specified will search path.

###Code to interegate search page
#driver.get('http://maps.co.blaine.id.us:8008/search/search.html');
#time.sleep(3) # Let the user actually see something!
#search_box = driver.find_element_by_id('txtSearch')


def getElementIDS():
    ###function to find all elements on page
    ans = []
    ids = driver.find_elements_by_xpath('//*[@id]')
    for ii in ids:
        #print ii.tag_name
        ans.append(ii.get_attribute('id'))    # id name as string
    return ans

#search_box = driver.find_element_by_id('txtSearch')
#search_box.send_keys('RP1M0000001580')
#search_box.send_keys(Keys.RETURN)



#APN_list = ['RP1M0000001570']
APN_list = df[['OBJECTID','APN']].values
#APN_list = APN_list[0:10]

text_list = []

count = 0
for APN in tqdm(APN_list):
    count += 1
    print(count)
    driver.get('http://maps.co.blaine.id.us:8008/blaine/rescharinfo.php?rp=' + APN[1])
    page = driver.page_source
      
    if 'Residential Characteristic Records:' in page:
        residential = page.split('<br />')[1].split(':')[-1]
    else:
        residential = 0
            
    if 'Manufactured Characteristic Records:' in page:
        manufactured = page.split('<br />')[2].split(':')[-1]
    else:
        manufactured = 0
    
    
    text_list.append([APN[0], APN[1], residential, manufactured, page])    
    

resultDF = pd.DataFrame(text_list)

resultDF.to_csv(savePath, index=False, header= ['OBJECTID','APN','RESIDENTIAL','MANUFACTURED','PAGE'])


#time.sleep(5) # Let the user actually see something!
driver.quit()