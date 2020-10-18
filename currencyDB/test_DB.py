from os import path
import pytest
from currencyDB import *
DB_FILE = r'/mnt/sdb1/python/exchangerateapi/currencyDB/currencyRate.db'


def test_create_db():
    create_db(DB_FILE)
    assert path.exists(DB_FILE)


def get_tables():
    con = create_connection(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    res = [tab[0] for tab in cur.fetchall()]
    con.close()
    return res


def test_create_tables():
    all_curs = [code + '_cur' for code in Exchange().get_all_rates().keys()]
    create_tables(DB_FILE)
    assert all_curs == get_tables()


