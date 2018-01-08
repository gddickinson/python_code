# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 08:59:17 2017

@author: George
"""

import urllib
import os
import sys
import time


try:
	from bs4 import BeautifulSoup
except ImportError:
	print ("[*] Please download and install Beautiful Soup first!")
	sys.exit(0)

#url = input("[+] Enter the url: ")
#download_path = input("[+] Enter the download path in full: ")

#url = r'https://www.lcrmscp.gov/steer_committee/work_tasks.html'
#url = r'https://www.lcrmscp.gov/crab/crab.html'
url = r'https://www.lcrmscp.gov/crtr/crtr.html'
#file_path = r'/Users/george/Desktop/LCR_powerpoints'
file_path = r'C:\Users\George\Desktop\LCR_Powerpoints'
files_in_dir = os.listdir(file_path)
number_files = len(files_in_dir)
download = urllib.request.URLopener()
missed = []
i = 0

try:
    while i < 10000:
        
        #to make it look legit for the url
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"} 
    
        request = urllib.request.Request(url, None, headers)
        html = urllib.request.urlopen(request)
        soup = BeautifulSoup(html.read(), "lxml") #to parse the website
        
        for tag in soup.findAll('a', href=True): #find <a> tags with href in it so you know it is for urls
            #so that if it doesn't contain the full url it can the url itself to it for the download
            tag['href'] = urllib.parse.urljoin(url, tag['href'])       
            #this is pretty easy we are getting the extension (splitext) from the last name of the full url(basename)
            #the spiltext splits it into the filename and the extension so the [1] is for the second part(the extension)
            if os.path.splitext(os.path.basename(tag['href']))[1] == '.pdf':
                try:
                    current = urllib.request.urlopen(tag['href'])
                except:
                    print ('error 1')
                    missed.append(tag['href'])
                    pass
                #header = current.info() 
                #print(str(header))
                print(tag['href'])
                if os.path.basename(tag['href']) in files_in_dir:
                    pass
                else:
                    
                    print ("\n[*] Downloading: %s" %(os.path.basename(tag['href'])))
                    
                    download_path = os.path.join(file_path,os.path.basename(tag['href']))
                    
                    print("\n[*] Download path: %s" % download_path)
        
                    with open(download_path,'wb') as f:
                        f.write(current.read())
                        #output.write(f)
        #
        #            #f = open(download_path + "\\" +os.path.basename(tag['href']))
        #            #f.write(current.read())
        #                f.close()
                    try:
                        download.retrieve(tag['href'], download_path)
                    except:
                        print('error 2')
                        missed.append(tag['href'])
                        i-=1
        
                i+=1
                print(i)
                time.sleep(0.01)
    
        print ("\n[*] Downloaded %d files" %(i+1))
    
except KeyboardInterrupt:
	print("[*] Exiting...")
	sys.exit(1)
    
except:
	print("I don't know the problem!")
	sys.exit(3)