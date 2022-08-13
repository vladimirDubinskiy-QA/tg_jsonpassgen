# подключение библиотеки telebot
# В google colab добавить: !pip install pyTelegramBotAPI
# для установки необходимо в файл requirements.text добавить строку
# 'PyTelegramBotApi'
from telebot import TeleBot, types
import json
import random

bot = TeleBot(token='5432270499:AAF9Ea0nApNPfmzsr9gpLhOcwGOo4BuEAT0', parse_mode='html')  # создание бота
body = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';:^#.,"  # Набор, из которого собираем пароль
length = 16  # Длина пароля
password = ""

# объект клавиаутры
card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
card_type_keybaord.row(
    types.KeyboardButton(text='Сгенерировать пароль'),
)


# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    bot.send_message(
        chat_id=message.chat.id,  # id чата, в который необходимо направить сообщение
        text='Привет! Я умею проверять JSON и форматировать его в красивый текст, а ещё могу сгенерировать '
             'пароль.\nПришли мне JSON в виде строки, напиши слово passgen или нажми "Сгенерировать пароль". ', 
        # текст сообщения
        reply_markup=card_type_keybaord,
    )


@bot.message_handler()
def message_handler(message: types.Message):
    if (message.text == "Сгенерировать пароль") or (message.text == "passgen"):  # Отдельно отлавливаем эти две фразы
        password = "".join(random.sample(body,
                                         length))  # Выбираем из переменной body случайные символы в кол-ве, заданном
                                                   # в переменной length 
        bot.send_message(message.chat.id, text=password)

    else:
        try:
            # а уже потом пытаемся распарсить JSON из текста сообщения
            payload = json.loads(message.text)
            text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
            bot.send_message(
                chat_id=message.chat.id,
                text=f'JSON:\n<code>{text}</code>'
            )
        except json.JSONDecodeError as ex:
            # при ошибке возникнет исключение 'json.JSONDecodeError'
            # преобразовываем исключение в строку и выводим пользователю
            bot.send_message(
                chat_id=message.chat.id,
                text=f'При обработке произошла ошибка:\n<code>{str(ex)}</code>'
            )
            return


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
