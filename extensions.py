import requests
from config import ACCESS_KEY

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        keys = {
            "доллар": "USD",
            "евро": "EUR",
            "рубль": "RUB"
        }

        if base not in keys:
            raise APIException(f"Валюта {base} не найдена.")
        if quote not in keys:
            raise APIException(f"Валюта {quote} не найдена.")
        if base == quote:
            raise APIException(f"Нельзя конвертировать валюту саму в себя.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Количество {amount} должно быть числом.")

        base_ticker = keys[base]
        quote_ticker = keys[quote]
        url = (
            f"https://api.exchangerate.host/convert?"
            f"from={base_ticker}&to={quote_ticker}&amount={amount}&access_key={ACCESS_KEY}"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка успешного ответа
            data = response.json()

            # Отладочный вывод
            print(f"Ответ API: {data}")

        except requests.exceptions.RequestException:
            raise APIException("Ошибка подключения к API.")
        except ValueError:
            raise APIException("Ошибка обработки ответа API.")

        # Извлечение курса
        result = data.get("result")
        if result is None:
            raise APIException("Ошибка получения данных о валюте.")

        return round(result, 2)
