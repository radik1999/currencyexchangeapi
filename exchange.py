import sqlite3
import ccy
import geocoder
import requests


class BaseCurrencyError(Exception):
    pass


class AmountError(Exception):
    pass


class Exchange:
    """Клас для отримання курсу валют"""

    def __init__(self, url='https://api.exchangerate.host/latest'):
        self.url = url
        self.all_rates = self.take_rates()
        self.all_rates_codes = list(self.all_rates)

    def take_rates(self):
        req = requests.get(self.url)
        return dict(req.json()['rates'])

    def get_all_rates(self, base='USD') -> dict:
        """Повертає курс по всіх можливих валютах в даній апі"""
        return {code: self.get_currency_rate(base, code) for code in self.all_rates_codes}

    def get_specific_rate(self, base, currency_codes, amount) -> object:
        if base.upper() not in self.all_rates_codes:
            raise BaseCurrencyError('There is no such currency')
        if amount < 1:
            raise AmountError('Amount must be 1 or more')
        res = {currency: rate * amount
               for currency, rate in self.get_all_rates(base).items()
               if currency in currency_codes}
        return res

    def get_exact_currency_rate(self, cur_from, cur_to):
        """
        cur_from: валюта продажу
        cur_to: валюта придбання
        повертає курс по конкретній валюті
        get_exact_currency_rate('usd', 'rub') = скільки потрібно віддати рублів за 1 долар
        """
        cur_from = cur_from.upper()
        cur_to = cur_to.upper()
        res = 0
        try:
            res = self.all_rates[cur_to] / self.all_rates[cur_from]
        except Exception as e:
            print(e)
        return res

    def get_currency_rate(self, cur_from, cur_to):
        """
        робить то саме що get_exact_currency_rate але округлює до 4 знака після коми
        """
        return round(self.get_exact_currency_rate(cur_from, cur_to), 4)

    def get_all_rate_by_country_code(self, country_code):
        """
        повертає курс по коду валюти країни(country_code)
        """
        res = {}
        for currency in self.all_rates:
            res[currency] = self.get_currency_rate(currency, country_code)
        return res

    def get_currency_by_living_place(self):
        """
        повертає курс по валюті країни з якої робиться запрос
        """
        current_country = geocoder.ip('me').country
        currency_code_of_current_country = ccy.countryccy(current_country)
        return self.get_all_rate_by_country_code(currency_code_of_current_country)


class DatabaseExchange(Exchange):
    def __init__(self, db_file=r'./currencyRate.db',
                 table_name='currency_rate'):
        self.db_file = db_file
        self.table_name = table_name
        super().__init__()

    def take_rates(self):
        records = None
        try:
            connection = sqlite3.connect(self.db_file)
            curs = connection.cursor()
            curs.execute(f'''select * from {self.table_name}''')
            records = curs.fetchall()

        except Exception as e:
            print(e)
        return dict(records)


if __name__ == '__main__':
    cur = DatabaseExchange()
