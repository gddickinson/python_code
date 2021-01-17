# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 16:32:38 2020

@author: g_dic
"""
### First run SQL file to create a database named sm_gw
### This can be done using MySQL Workbench

import mysql.connector
import pandas as pd

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Jester100",
  use_pure=True,
  database="sm_gw"

)


cursor = db.cursor()

##Get database names
# ## executing the statement using 'execute()' method
# cursor.execute("SHOW DATABASES")

# ## 'fetchall()' method fetches all the rows from the last executed statement
# databases = cursor.fetchall() ## it returns a list of all databases present

# ## printing the list of databases
# print(databases)

# ## showing one by one database
# for database in databases:
#     print(database)

# #get tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# #get fieldnames for tables
# fieldNameDict = {}

# for table in tables:
#     cursor.execute('SELECT * FROM {}'.format(table[0]))
#     table_rows = cursor.fetchall()
#     fieldNameDict.update({table[0]:cursor.column_names})    


# #Extract data to pd dataframe
# cursor.execute('SELECT * FROM gws_output')
# table_rows = cursor.fetchall()
# df = pd.DataFrame(table_rows, columns=cursor.column_names)
# df.head()

#Save all tables to csv
for table in tables:
    cursor.execute('SELECT * FROM {}'.format(table[0]))
    table_rows = cursor.fetchall()
    df = pd.DataFrame(table_rows, columns=cursor.column_names)
    filename = r'C:\Users\g_dic\OneDrive\Desktop\Soil Salinity 202006\{}.csv'.format(table[0])
    df.to_csv(filename)
    print('{} Done'.format(table[0]))


