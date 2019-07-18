# -*- coding: utf-8 -*-
import sys
import os
import nse_analyzer.scrapper as nse
from datetime import date,timedelta
import configparser
#print("""Adios, welcome to the script to download Combined Open interest across exchanges
#      downloader\n There are two ways of using this script\n\n
#      1. To do an incremental download or delta download - which will get today's latest file \n
#      2. To do a historic download of data using "python nse_analyzer {date ranges in ddmmYYYY format}\n\n"""
#      )
w=nse.Wrapper()
try:
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),'nse_config.ini'))
#    print(os.path.join(os.getcwd(), 'nse_config.ini'))
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

