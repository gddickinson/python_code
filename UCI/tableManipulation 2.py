# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 09:19:11 2019

@author: George
"""

#import pandas library
import pandas as pd

#define path to data file
fileName = r"C:\Users\George\Dropbox\UCI\ian_smith\Book1.xlsx"
savePath = r"C:\Users\George\Dropbox\UCI\ian_smith\result.csv"

#import data as dataframe
df = pd.read_excel(fileName)

#check data loaded by showing first 5 rows
print(df.head(n=5))

#remove unwanted columns using list of col names (define axis =1 to select columns instead of rows)
df = df.drop(['TimeLapseIndex','Entity','MaxFoverF0'], axis=1)

#show new df header
print(df.head(n=5))

#group by time using dataframe groupby function and then aggregate grouped columns to lists (using lambda function to apply list to both columns) 
groupDF = df.groupby('Time[s]').agg(lambda x: list(x))

#now two columns ObjectId, FoverF0 with time as row names
print(groupDF.head(n=5))

#check lengths of ObjectID lists and FoverF0 - use mapping function to apply len() to every cell in dataframe
lengths = groupDF.applymap(lambda x: len(x))
print(lengths)
maxNum = max(lengths['ObjectId'])

#differnt lengths of lists for each time - so cannot create new dataframe with without adding NA values
#create new df by expanding each cell list (use apply to expand using pd.Series to each row of 'FoverF0')
finalDF = pd.DataFrame(groupDF['FoverF0'].apply(pd.Series))

#rename the columns using longest ObjectId list (as ObjectIDs just a number series would be easier just to rename using values 1:maxNum - but for more robust code actually getting the ColumnID values)

#get ID of a row with longest number of values
longestTimeRow = (lengths.loc[lengths['ObjectId'] == maxNum]).iloc[0].name

#use ID to get list of column names (select row using .loc)
nameList = groupDF['ObjectId'].loc[longestTimeRow]

#rename finalDF columns using nameList
finalDF.columns = nameList

#export finalDF as csv
finalDF.to_csv(savePath)


