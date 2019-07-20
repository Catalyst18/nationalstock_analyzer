import psycopg2
from sqlalchemy import create_engine
import io
from pandas import DataFrame as df
import csv
class DatabaseManager:
    def __init__(self,user,password,host,port,database):
        try:
            self.connection = psycopg2.connect(
                user = user,
                password = password,
                host = host,
                port = port,
                database = database
            )
            self._cursor = self.connection.cursor()
            print('Connection is successful')
        except (Exception,psycopg2.Error) as e:
            print('Error in establishing a connection',e)
        # finally:
            # self._cursor.close()
            # self.connection.close()
    def close_connection(self):
        if self.connection:
            try:
                self._cursor.close()
                self.connection.close()
            except Exception as e:
                print('Unable to close connection',e)
            print('Closed the connection successfuly')

    
    def select_data(self,query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.records = self.cursor.fetchall()
        return self.records
    
    def pd_to_postgres(self,table_name,df):
        #Create a connection engine
        self.engine = create_engine('postgres://postgres:Etsantosh_18@localhost:5432/postgres')
        #truncate the table as this is a staging table
        self.engine.execute('TRUNCATE TABLE nse_analyzer.{}'.format(table_name))
        print('\ntruncated {}'.format(table_name))
        # Establish a raw connection to load dataframe into postgres database
        self.sqlalchemy_conn = self.engine.raw_connection()
        self.sqlalchemy_cursor = self.sqlalchemy_conn.cursor()
        self.output = io.StringIO()
        df.to_csv(self.output,sep=',',header = False,index = False)
        self.output.seek(0)
        self.contents = self.output.getvalue()
        print(self.contents)
        self.sqlalchemy_cursor.copy_from(self.output,'nse_analyzer.stage_raw_nse_data',sep=',')
        self.sqlalchemy_conn.commit()
        # self.connection.commit()
        # self.engine.dispose()
        
        self.insert_count=self.engine.execute('select count(*) from nse_analyzer.{}'.format(table_name))
        print('{} Records inserted sucessfully'.format(self.insert_count))
        