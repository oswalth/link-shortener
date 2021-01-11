import telebot
import config
import utils
import re
import os
import setup
from telebot import types
from flask import Flask, request

setup.launch_db()

bot = telebot.TeleBot(config.TOKEN)
server = Flask(__name__)

# Слушаем команду  старт, чтобы приветствовать юзера
@bot.message_handler(commands=["start"])
def welcome(message):
    sti = open("./static/sticker.webp", 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
      "Привет {}. Отправь мне ссылку, а я верну тебе укороченный вариант".format(message.from_user.first_name),
      parse_mode="html")

# Слушаем команду history, чтобы отдать 10 последних ссылок
@bot.message_handler(commands=["history"])
def get_links_history(message):
    response = utils.select_links(message)
    bot.send_message(message.chat.id, response, disable_web_page_preview=True)

# Слушаем любые текстовые сообщения
@bot.message_handler(content_types=['text'])
def shorten_link(message):

    # Добавляем кнопку показа 10 последних ссылок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/history"))

    # Выделяем из сообщения только ссылки
    links = re.findall("(?P<url>https?://[^\s]+)", message.text)

    # Формируем ответ бота в виде <ссылка> - <короткая_ссылка>
    response = utils.shorten_links(links, message.chat.id)
    # Отправляем итоговый ответ пользователю, скрывая превью веб-страницы
    bot.send_message(message.chat.id, response, disable_web_page_preview=True, reply_markup=markup)


@server.route('/' + config.TOKEN, methods=['POST'])
def recieveMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://fathomless-bastion-55645.herokuapp.com/" + config.TOKEN)
    return '!', 200

print('Bot is running...')
# Бот слушает в режиме нон-стоп 
if __name__ == '__main__':
    # bot.polling()
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

