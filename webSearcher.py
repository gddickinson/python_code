# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:52:58 2019

@author: George
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

def unique(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

#set search term
search_query_list = ["plastic surgeon CA", "plastic surgeon california", "cosmetic surgeon CA", "plastic surgeon LA",
                     "plastic surgeon orange county", "cosmetic surgeon LA", "cosmetic surgeon orange county"]


#set chromedriver path
executable_path = "C:\chromedriver.exe"


#make list for results
resultsList = []


for search_query in search_query_list:
    #open browser
    browser = webdriver.Chrome(executable_path=executable_path)
    opts = Options()
    opts.set_headless()
    assert opts.headless  # Operating in headless mode
    browser.get('https://duckduckgo.com')
    search_query = search_query.replace(' ', '+') #structuring our search query for search url.
    #run search term
    search_form = browser.find_element_by_id('search_form_input_homepage')
    search_form.send_keys(search_query)
    search_form.submit()
    
    #keep clicking more results button to get all results
    for i in range(1,50):
        try:    
            results_button = browser.find_element_by_id('rld-'+str(i))
            results_button.click()
            print(i)
            #sleep(0.5)
        except:
            pass
    
    #get results
    results = browser.find_elements_by_class_name('result')
    
    #compile results containing .com into list
    for result in results:
        if '.com' in result.text:
            resultsList.append(result.text)
            
    #close browser
    browser.close()

#filter for unique results
filteredResults = unique(resultsList)

#extract address from text
addressList = []

for result in filteredResults:
    addressList.append(result.split('\n')[1])




