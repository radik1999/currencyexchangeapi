import sqlite3
from sqlite3 import Error


def create_db(file='./currencyRate.db'):
    """
    create db file if it doesn't exist and connect to the db
    """
    connection = None
    try:
        connection = sqlite3.connect(file)
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def create_tables(db_file='./currencyRate.db'):
    """
    create tables that will be containing currency rate by each currency code
    """
    from currencyDB.exchange import Exchange
    from currencyDB.dbTools import create_connection

    sql_create_table = '''create table if not exists {table_name} (
                            code text not null primary key,
                            rate real);'''

    try:
        connection = create_connection(db_file)
        cursor = connection.cursor()

        all_codes = Exchange().get_all_rates().keys()  # getting all currency codes

        for code in all_codes:
            code = code + '_cur'
            cursor.execute(sql_create_table.format(table_name=code))

        connection.close()

    except Exception as e:
        print(e)


