import telebot

from config import currency, TOKEN
from utils import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту:\n<Наименование валюты>\n<в какую валюту перевести>\n<количество>\n' \
           'Посмотреть список доступных валют: /values\n'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for cur in currency.keys():
        text = '\n'.join((text, cur,  ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConvertionException('Вы ввели больше трех параметров. Повторите ввод в формате: \n' \
                                      '<Наименование валюты> <в какую валюту перевести> <количество>\n')
        if len(values) < 2:
            raise ConvertionException('Вы ввели меньше двух параметров. Повторите ввод.')
        elif len(values) == 2:
            values.append('1')


        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base,amount)
        convertion_result = round(( float(amount) * total_base), 2)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Курс {quote} к {base} = {total_base}\n Для покупки {amount} {quote} потребуется {convertion_result} {base}     '
        print(text)
        bot.send_message(message.chat.id, text)


print('КриптоБотчик начинает свою работу :)')

bot.polling()