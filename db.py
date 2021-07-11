import sqlite3
from sqlite3 import Error

class Db:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()

    def create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print('database connection created, sqlite version: {0}'.format(sqlite3.version))
        except Error as e:
            print(e)
        
        self.conn = conn
        return conn

    def create_table(self, create_table_sql):
        conn = self.conn
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
        return
