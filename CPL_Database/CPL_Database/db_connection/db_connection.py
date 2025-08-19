import pyodbc
import logging
import pandas as pd

class DataBase_Connection:
    def __init__(self, 
                server = 'p-fundmaster-dbserver.database.windows.net',
                database = 'FundMaster',
                username = 'prodromos.thom@email.com',
                authentication = 'ActiveDirectoryInteractive',
                driver = '{ODBC Driver 17 for SQL Server}'):
        self.server = server
        self.database = database
        self.username = username
        self.authentication = authentication
        self.driver = driver
        self.conn = None

    def connect(self):
        '''
        The function returns a connection for the database.
        '''
        try:
            self.conn = pyodbc.connect(
                'DRIVER=' + self.driver +
                ';SERVER=' + self.server +
                ';PORT=1433;DATABASE=' + self.database +
                ';UID=' + self.username +
                ';AUTHENTICATION=' + self.authentication
            )
            # print("Successful connection to database!")
        except pyodbc.Error as e:
            print(f"Connection to database failed: {e}")
        return self.conn
    
    def get_cursor(self) -> pyodbc.Cursor:
        '''
        The function returns a cursor for the database connection.
        '''
        if self.conn is None:
            print("Connection is not established. Trying to connect...")
            self.connect()
        if self.conn:
            return self.conn.cursor()
        else:
            raise ConnectionError("Failed to establish a database connection.")


    def close_connection(self):
        '''
        The function closes the database connection.
        '''
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def execute_query_to_df(self, query: str) -> pd.DataFrame:
            '''
            The function executes a given SQL query and returns the results as a DataFrame.
            '''
            cursor = self.get_cursor()
            try:
                cursor.execute(query)
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                df = pd.DataFrame.from_records(rows, columns=columns)
                return df
            except pyodbc.Error as e:
                print(f"Failed to execute query: {e}")
                return pd.DataFrame()


    def get_table(self, table_name: str) -> pd.DataFrame:
        '''
        The function returns all rows from the specified table as a pandas DataFrame.
        '''
        query = f"SELECT * FROM {table_name}"
        try:
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            logging.error(f"Failed to fetch FundMaster data from table {table_name}: {e}")
            print(f"Failed to fetch data from table {table_name}: {e}")
            return pd.DataFrame()