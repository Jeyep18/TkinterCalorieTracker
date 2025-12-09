import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host = os.getenv("DB_HOST"),
                    user = os.getenv("DB_USER"),
                    password = os.getenv("DB_PASSWORD"),
                    database = os.getenv("DB_NAME")
                )
                print("Database connection established.")
                return True
            except Error as e:
                print(f"Error connecting to database: {e}")
                return False
        return True
    
    def get_connection(self):
        if not self.connect():
            raise Exception("Unable to connect to the database.")
        return self._connection
    
    def execute_query(self, query, params = None, fetch = False):
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary = True)
            cursor.execute(query, params or ())

            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                connection.commit()
                last_id = cursor.lastrowid
                cursor.close()
                return last_id
            
        except Error as e:
            print(f"Error executing query: {e}")
            raise

    def execute_many(self, query, data):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.executemany(query,data)
            connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing multiple queries: {e}")
            return False
    
    def initialize_database(self):
        try:
            with open('database/schema.sql', 'r') as file:
                schema = file.read()
            
            statements = schema.split(';')

            for statement in statements:
                if statement.strip():
                    self.execute_query(statement)
            
            print("Database initialized successfully.")
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
        
    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Database connection closed.")

