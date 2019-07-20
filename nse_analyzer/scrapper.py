# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import date,timedelta
import requests
# import shutil
import sys

class Wrapper:
    def __init__(self):
        pass
    
    def download_data(self,date,path):
        """date in ddmmyyyy format is passed as the argument"""
#        print('new')
        self._date = date
        self._url='https://www.nseindia.com/archives/nsccl/mwpl/combineoi_{}.zip'.format(self._date)
        self._file_cache = requests.get(self._url)
        with open(path+'\\combine_{}.zip'.format(self._date),'wb') as f:
            f.write(self._file_cache.content)
        print('The file combine_{} is persisted in the following directory {}'.format(self._date,path))
        return(path+'\\combine_{}.zip'.format(self._date),'combineoi_{}.csv'.format(self._date))


