import ccy
import geocoder
import requests
from pprint import pprint

class Exchange:
    """Клас для отримання курсу валют"""

    def __init__(self, url='https://api.exchangerate.host/latest'):
        self.url = url
        self.all_rates = self.get_all_rates()

    def get_all_rates(self, base='USD') -> list:
        """Повертає курс по всіх можливих валютах в даній апі"""
        self.parameters = {'base': base}
        req = requests.get(self.url, params=self.parameters)
        return req.json()['rates']

    def get_exact_currency_rate(self, cur_from, cur_to):
        """
        cur_from: валюта продажу
        cur_to: валюта придбання
        повертає курс по конкретній валюті
        get_exact_currency_rate('usd', 'rub') = скільки потрібно віддати рублів за 1 долар
        """
        cur_from = cur_from.upper()
        cur_to = cur_to.upper()
        if cur_to not in self.all_rates:
            return f'There isn\'t {cur_to} currency'
        if cur_from not in self.all_rates:
            return f'There isn\'t {cur_from} currency'

        return self.all_rates[cur_to] / self.all_rates[cur_from]

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


if __name__ == '__main__':
    cur = Exchange()
    pprint(cur.get_all_rates('UAH'))

