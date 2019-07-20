# -*- coding: utf-8 -*-
import sys
import os
import nse_analyzer.scrapper as nse
from datetime import date,timedelta
import configparser
import nse_analyzer.data_integration as di
import pandas as pd
from pandas import DataFrame as df

print("""Adios, welcome to the script to download Combined Open interest across exchanges downloader
     \n There are two ways of using this script\n
     1. To do an incremental download or delta download - which will get today's latest file \n
     2. To do a historic download of data using "python nse_analyzer {date ranges in ddmmYYYY format}\n""")
w=nse.Wrapper()
try:
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),'nse_config.ini'))
    # print(os.path.join(os.getcwd(), 'nse_config.ini'))
    path = config.get('config','directory')
except Exception as e:
    print(e)
#print(path)

#print(sys.argv[1:])
if len(sys.argv[1:]) == 0:
    print(sys.argv[0])
    print('"""""""""""""""""""')
    date_to_extract = date.today()-timedelta(1)    
    date_to_extract = date_to_extract.strftime('%d%m%Y')
    w.download_data(date_to_extract,path)
for date_range in sys.argv[1:]:
    w.download_data(date_range,path)
#    print(date_range)
try:    
    d = di.DatabaseManager('postgres','Etsantosh_18','localhost','5432','postgres')
    records=d.select_data('select * from nse_analyzer."D_NSE_COMPANIES"')
    print('\n{}\n'.format(records))
    # d.close_connection()
    # d.pd_to_postgres()
except Exception as e:
    print(e)

df = pd.read_csv('C:\\NSE_DATA_FOLDER\\combineoi_17072019.csv')
df.columns = ['report_date','isin_id','company_name','company_symbol','mwpl_amount','open_interest','limit_amount']
df.loc[df['limit_amount']=='No Fresh Positions','limit_amount']=0
# df[['REPORT_DATE']] = df[['REPORT_DATE']].apply(pd.to_datetime)
df[['limit_amount']] = df[['limit_amount']].apply(pd.to_numeric)
d.pd_to_postgres('stage_raw_nse_data',df)
# d.close_connection()
