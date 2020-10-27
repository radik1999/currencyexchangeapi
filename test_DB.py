import os
from dbTools import *
DB_FILE = r'./currencyRate.db'


def test_create_db():
    with Database(DB_FILE) as connection:
        pass
    assert os.path.exists(DB_FILE)


def get_tables():
    with Database(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = [tab[0] for tab in cur.fetchall()]
    return res


def test_create_tables():
    created = False
    with Database(DB_FILE) as con:
        cur = con.cursor()
        create_table(con, 'test')
        created = 'test' in get_tables()
        cur.execute('drop table test;')
    assert created


def test_insert_record():
    table_name = 'currency_rate'
    inserted = False
    with Database(DB_FILE) as con:
        cur = con.cursor()

        params = ('test', 322)
        insert_record(con, params, table_name)
        cur.execute(f'''select * from {table_name} where code='{params[0]}';''')
        inserted = params == cur.fetchone()
        cur.execute(f'''delete from {table_name} where code='{params[0]}';''')
        con.commit()
    assert inserted


def test_update_record():
    updated = False
    table_name = 'currency_rate'
    with Database(DB_FILE) as con:
        cur = con.cursor()
        record = ('test', 322)
        cur.execute(f'''insert into {table_name}(code, rate) values(?, ?)''', record)

        update_record(con, record[0], 300, table_name)
        cur.execute(f'''select * from {table_name} where code='{record[0]}';''')

        updated = (record[0], 300) == cur.fetchone()

        cur.execute(f'''delete from {table_name} where code='{record[0]}';''')
        con.commit()
    assert updated


if __name__ == '__main__':
    test_create_db()
    test_create_tables()
    test_insert_record()
    test_update_record()
