import psycopg2

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
    
     