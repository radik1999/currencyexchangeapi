from fastapi import FastAPI
from datetime import date

from intervalUpdateDB import daily_update_db
from currencyDB import DatabaseExchange

app = FastAPI()
daily_update_db()


@app.get('/')
def retrieve_currency_rate_by_code(base: str = 'USD', codes: str = None, amount: int = 1):
    db = DatabaseExchange()
    specific_currencies_rate = db.get_specific_rate(base, codes, amount)
    res = {
        'base': base,
        'amount': amount,
        'date': date.today(),
        'currencies rate': specific_currencies_rate
    }
    return res
