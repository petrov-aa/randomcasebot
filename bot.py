import os
import random
import re

import telebot
from telebot import types

filters = [
    lambda l: "<b>" + l + "</b>",
    lambda l: "<i>" + l + "</i>",
    lambda l: "<code>" + l + "</code>",
    lambda l: "<u>" + l + "</u>",
    lambda l: l.upper(),
]

prev_filter = None

def random_style_letter(letter):
  global prev_filter
  if not re.match(r'[А-яЁёA-z]', letter):
  	return letter
  try_filters = list(filter(lambda f: f is not prev_filter, filters))
  prev_filter = fil = random.choice(try_filters)
  return fil(letter.lower())
  
def random_style_text(text):
	letters = list(text)
	return " ".join(map(random_style_letter, letters))

print(random_style_text("Hello there!"))


bot = telebot.TeleBot(os.environ("BOT_TOKEN"));

@bot.message_handler(commands=['start', 'help'])
def on_start(message):
  bot.reply_to(message, "Привет, я случайным способом меняю текст с такого вот на такой")

@bot.message_handler(content_types=['text'])
def on_text(message):
  bot.reply_to(message, "Привет, я случайным способом меняю текст с такого вот на такой")

@bot.inline_handler(lambda query: True)
def on_inline(inline_query):
  styled_text = random_style_text(text)
  r = types.InlineQueryResultArticle(styled_text, styled_text, types.InputTextMessageContent(styled_text))

bot.polling(none_stop=True, interval=9999)

