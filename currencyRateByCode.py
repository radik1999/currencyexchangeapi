from pprint import pprint

from currencyDB import DatabaseExchange


def get_rate(currency_dode: str) -> dict:
    """
    :param currency_dode:
    :return: currency rate by currency_code
    """
    de = DatabaseExchange()
    return {'currency base': currency_dode, 'currency rates': de.get_all_rates(currency_dode)}


