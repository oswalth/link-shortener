import telebot
import config
import requests
import json
import os
from telebot import types

chat_history = {}


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):

  

  sti = open("./static/sticker.webp", 'rb')
  bot.send_sticker(message.chat.id, sti)
  bot.send_message(message.chat.id, 
    "Привет {}. Отправь мне ссылку, а я верну тебе укороченный вариант".format(message.from_user.first_name), 
    parse_mode="html")
  chat_history[message.chat.id] = []


@bot.message_handler(commands=["history"])
def get_links_history(message):
  if chat_history:
    response = "\n".join([link for link in chat_history[message.chat.id][-10:]])
    bot.send_message(message.chat.id, response)


@bot.message_handler(content_types=['text'])
def shorten_link(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(types.KeyboardButton("/history"))

  response = requests.post(config.SHORTENER_LINK, {"url": message.text})
  if (response.status_code == 400):
    bot.send_message(message.chat.id, "Неверный адрес, попробуйте заново.")
  else:
    short_link = f"{config.SHORTENER_PREFIX}{response.json()['hashid']}"
    bot.send_message(message.chat.id, short_link,
    reply_markup=markup)
    if short_link not in chat_history[message.chat.id]:
      chat_history[message.chat.id].append(short_link)


bot.polling(none_stop=True)