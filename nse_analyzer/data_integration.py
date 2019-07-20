import psycopg2
import io
from pandas import DataFrame as df

class DatabaseManager:
    def __init__(self,user,password,host,port,database):
        try:
            self._connection = psycopg2.connect(
                user = user,
                password = password,
                host = host,
                port = port,
                database = database,
            )
            self._cursor = self._connection.cursor()
            print('Connection is successful')
        except (Exception,psycopg2.Error) as e:
            print('Error in establishing a connection',e)
        # finally:
        #     self._cursor.close()
        #     # self.connection.close()
    def close_connection(self):
        if self._connection:
            try:
                self._cursor.close()
                self._connection.close()
            except Exception as e:
                print('Unable to close connection',e)
            print('Closed the connection successfuly')

    
    def select_data(self,query):
        # self.cursor = self.connection.cursor()
        self._cursor.execute(query)
        self.records = self._cursor.fetchall()
        return self.records
    
    def pd_to_postgres(self,schema_name,table_name,df):
        self.data = io.StringIO()
        df.to_csv(self.data,sep=',',header=False,index=False)
        self.data.seek(0)
        self._cursor.copy_from(self.data,'{}.{}'.format(schema_name,table_name),sep=',')
        self._connection.commit()
        