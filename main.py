import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# @bot.message_handler()
# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'hello')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = (
        "Добро пожаловать! Я бот для конвертации валют.\n"
        "Чтобы узнать курс, отправь сообщение в формате:\n"
        "<имя валюты, цену которой хочешь узнать> "
        "<имя валюты, в которой хочешь узнать цену> "
        "<количество>\n"
        "Пример: доллар рубль 100\n\n"
        "Список доступных валют: /values"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    currencies = ['доллар', 'евро', 'рубль']  # Список доступных валют
    text = "Доступные валюты:\n" + "\n".join(currencies)
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException("Неверный ввод. Укажи три параметра.")
        base, quote, amount = values
        result = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"Что-то пошло не так: {e}")
    else:
        text = f"Цена {amount} {base} в {quote} — {result}"
        bot.reply_to(message, text)

bot.polling()
