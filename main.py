from fastapi import FastAPI

from intervalUpdateDB import daily_update_db
import currencyRateByCode


app = FastAPI()
# daily_update_db()


@app.get('/rate')
def retrieve_currency_rate_by_code(code: str):
    return currencyRateByCode.get_rate(code)
