import sqlite3
from sqlite3 import Error


def create_connection(db_file='./currencyRate.db'):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        connection.close()
    return connection
