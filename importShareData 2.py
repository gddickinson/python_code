# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 19:10:07 2018

@author: George
"""

import quandl
import datetime
import pandas as pd
from matplotlib import pyplot as plt
 
quandl.ApiConfig.api_key = '7KxDcKvY1suwa_ZSfyxE'
 
def quandl_stocks(symbol, start_date=(2000, 1, 1), end_date=None):
    """
    symbol is a string representing a stock symbol, e.g. 'AAPL'
 
    start_date and end_date are tuples of integers representing the year, month,
    and day
 
    end_date defaults to the current date when None
    """
 
    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]
 
    start_date = datetime.date(*start_date)
 
    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()
 
    return quandl.get(query_list, 
            returns='pandas', 
            start_date=start_date,
            end_date=end_date,
            collapse='daily',
            order='asc'
            )
 

def getSymbols_SP500():
        symbols_table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                                 header=0)[0]
        return list(symbols_table.loc[:, "Ticker symbol"])
 
if __name__ == '__main__':
 
    symbols_SP500 = getSymbols_SP500()

    symbols_SP500 = symbols_SP500[0:10]
    
    
    apple_data = quandl_stocks('AAPL')
    print(apple_data)