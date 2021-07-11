import sqlite3
from sqlite3 import Error

class Db:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        

    def create_connection():
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        
        self.conn = conn
        return conn

   # def create_product(product_data):
        
