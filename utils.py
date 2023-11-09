import requests

import json

from config import currency


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote  == base:
            raise ConvertionException(f'Введены одинаковые валюты <<{base}>>\n' \
            'Посмотреть список доступных валют: /values\n')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f'Невозможно обработать валюту <<{quote}>>.\n' \
            'Посмотреть список доступных валют: /values\n')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f'Невозможно обработать валюту <<{base}>>.\n' \
            'Посмотреть список доступных валют: /values\n')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Неверный формат <<{amount}>>. \n' \
                    'Введите числовое значение суммы. \n' \
                    'Чтобы ввести дробное значение используйте точку (например, 0.68)')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        total_base = json.loads(r.content)[currency[base]]

        return total_base
    @staticmethod
    def get_total_base(values):
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
        text = f'Курс {quote} к {base} = {total_base}\n'
        return text