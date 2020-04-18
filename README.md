OVERVIEW: 

This is a Developement project for analyzing the National stock Exchange (NSE).
https://www.nseindia.com/products/content/derivatives/equities/homepage_fo.htm
The Idea of the project on the big picture is to have a historical data in the database at our disposal, on which we can run any time of analysis.

Phase I:
In this project the phase 1 is one can download the 'Combined Open Interest across Exchange' file on demand.
For those who have known these files are monthly summary reports of different exchange rates.
This cli-app downloads data on demand - (The idea is to have it run daily on batch which I am working on at the moment).
Finally it stores the data to Postgres database.

The Idea is to grow the database upto years and we can stay upto date on running some predictive analytics on them.

Prerequisites:

You would need a running Postgred Database for this.
You can download the latest version of POSTGRES11 here https://www.postgresql.org/download/

Once you have your Postgres up and running, get hold of the "nse_analyzer_model.sql" and run the scripts to create the necessary Database and relationships.

Note: If you wish to alter the schema name/ table name feel free to do so (I am not great in naming -lame).

You need python version > 3.x.x installed 
If you are on windows you can get it downloaded from here https://www.python.org/downloads/

If you are on Linux or Mac make sure the python version is > 3.x.x



INSTALLATION:

1.	Clone / Download the Git repository files https://github.com/Catalyst18/nationalstock_analyzer.git

2. 	Navigate to the downloaded folder into the directory 'nationalstock_analyzer'
	Once Inside run

	python setup.py install 

	The Installation will begin now and will install necessary dependencies ['psycopg2','pandas','configparser','requests'].

HOW TO ?:

Before we begin we need to setup the default.ini file with necessary parameters.

There are two ways of using this script

     1. To do an incremental download or delta download - which will get today's latest file.

     		$python nse_analyzer

     2. To do a historic download of data using "python nse_analyzer {date ranges in ddmmYYYY format}.
         eg : $python nse_analyser 01012017 31092019

WHATS NEXT?:

For Phase 2 & 3

I am planning to normalize the data in the data model tables.

Produce a report trend that has the stats of investments and stock market analysis.

Make the code more robust to download multiple dataset eg for Crude oil, natural gas, COMPANY specific historic trends

Predict the right time to buy or sell shares with Machine Learning.










