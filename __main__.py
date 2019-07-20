# -*- coding: utf-8 -*-
import sys
import os
import nse_analyzer.scrapper as nse
from datetime import date,timedelta
import configparser
import nse_analyzer.data_integration as di
import pandas as pd
from pandas import DataFrame as df
import zipfile

print("""Adios, welcome to the script to download Combined Open interest across exchanges downloader
     \n There are two ways of using this script\n
     1. To do an incremental download or delta download - which will get today's latest file \n
     2. To do a historic download of data using "python nse_analyzer {date ranges in ddmmYYYY format}\n
         eg:python nse_analyzer python nse_analyser 01012017 31092019""")

def load_data_to_db():    
    try:
        """
    **********************************************************************************************************
        Get config about the postgres database details
    **********************************************************************************************************
        """
        
        user_name = config.get('config','user')
        password =  config.get('config','password')
        host = config.get('config','host')
        port = config.get('config','port')
        database = config.get('config','database')
        schema = config.get('config','schema')
        table_name =config.get('config','table_name')
        """
    **********************************************************************************************************
        Load the data that is downloaded into postgres DB
    **********************************************************************************************************    
        """

        d = di.DatabaseManager(user_name,password,host,port,database)
        with zipfile.ZipFile(zip_file_path) as zf:
            with zf.open(csv_file_name) as f:
                df = pd.read_csv(f)
                df.columns = ['report_date','isin_id','company_name','company_symbol','mwpl_amount','open_interest','limit_amount']
                df.loc[df['limit_amount']=='No Fresh Positions','limit_amount']=0
                df[['limit_amount']] = df[['limit_amount']].apply(pd.to_numeric)
                #Create a column insert_time to log when the insert happens
                df['insert_time'] = pd.Series(pd.to_datetime('today'), index=df.index)
                d.pd_to_postgres(schema,table_name,df)
                # d.close_connection()
                # print(zip_file_path,csv_file_name)
    except Exception as e:
        print(e)
    finally:
        d.close_connection()

        
w=nse.Wrapper()
try:
    config = configparser.ConfigParser()
    if os.path.isfile('nse_config.ini'):
        config.read(os.path.join(os.getcwd(),'nse_config.ini'))
    else:
        config.read(os.path.join(os.getcwd(),'default.ini'))
    # print(os.path.join(os.getcwd(), 'nse_config.ini'))
    path = config.get('config','directory')
except Exception as e:
    print(e)
    
"""
**********************************************************************************************************
Main block below is to download the file from the nse engine
this is to persist the files of combined open interest across exchanges.
**********************************************************************************************************
"""
if len(sys.argv[1:]) == 0:
    print(sys.argv[0])
    print('"""""""""""""""""""')
    date_to_extract = date.today()-timedelta(1)    
    date_to_extract = date_to_extract.strftime('%d%m%Y')
    zip_file_path,csv_file_name = w.download_data(date_to_extract,path)
    load_data_to_db()
for date_range in sys.argv[1:]:
    zip_file_path,csv_file_name=w.download_data(date_range,path)
    load_data_to_db()
"""
**********************************************************************************************************
The below try catch block accomplishes two things
1.  It establishes the connections with postgres which requires postgres db
    As the file is downloaded in the above directory it takes the file and loads it
    to the specified schema and table
**********************************************************************************************************
"""


