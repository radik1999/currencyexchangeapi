import sqlite3
from sqlite3 import Error
from exchange import Exchange


class Database:
    """
    class that will help us to close connection when we'll be using command - "with"
    """

    def __init__(self, db_file=r'./currencyRate.db'):
        self.connection = sqlite3.connect(db_file)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def create_table(connection, table_name='currency_rate'):
    """
    create tables that will be containing currency rate by each currency code
    """

    sql_create_table = f'''create table if not exists {table_name} (
                            code text not null primary key,
                            rate real);'''

    cursor = connection.cursor()
    cursor.execute(sql_create_table)


def insert_record(connection, values, table_name='currency_rate'):
    """
    creating record into currency rate table
    :param connection:
    :param table_name:
    :param values: inserting into table_name parameters
    """

    sql_insert = f'''insert into {table_name}(code, rate) values(?,?)'''

    cursor = connection.cursor()
    try:
        cursor.execute(sql_insert, values)
        connection.commit()
    except Error as e:
        print(e)


def insert_all_records(connection, table_name='currency_rate'):
    """
    creating all record in currency rate table
    :param connection:
    :param table_name:
    :return:
    """
    exch = Exchange()

    for code, rate in exch.all_rates.items():
        pars = (code, rate)
        insert_record(connection, pars, table_name)


def update_record(connection, pk, parameter, table_name='currency_rate'):
    """
    update one record in certain currency table
    :param connection:
    :param table_name:
    :param pk: record needed to update
    :param parameter: a parameter that old parameter will be replaced
    :return:
    """
    cursor = connection.cursor()
    sql_update = f'''update {table_name}
                        set rate = {parameter}
                        where code = '{pk}';'''

    try:
        cursor.execute(sql_update)
        connection.commit()
    except Error as e:
        print(e)


def update_table(connection, table_name='currency_rate'):
    """
    updating whole table
    :param table_name:
    :param connection:
    :return:
    """

    exch = Exchange()
    for code, rate in exch.all_rates.items():
        update_record(connection, code, rate, table_name)


if __name__ == '__main__':
    with Database() as con:
        pass
