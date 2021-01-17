# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 20:01:15 2019

@author: George
"""


#https://health.usnews.com/doctors/plastic-surgeons
#https://health.usnews.com/doctors/gregory-levitin-66000?int=search_full_result_card_click_with_requestappointment

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

url = 'https://health.usnews.com/doctors/plastic-surgeons'
response = get(url)

soup = BeautifulSoup(response.text, 'html.parser')

soup.findAll('a')

one_a_tag = soup.findAll('a')[0]