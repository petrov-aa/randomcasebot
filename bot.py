import os
import random
import re
import hashlib

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

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])

@bot.message_handler(commands=['start', 'help'])
def on_start(message):
  bot.send_message(message.chat.id, "Привет. Я случайным способом меняю текст с такого вот на " + random_style_text("такой"), parse_mode="HTML")

@bot.message_handler(content_types=['text'])
def on_text(message):
  bot.send_message(message.chat.id, random_style_text(message.text), parse_mode="HTML")

@bot.inline_handler(lambda query: True)
def on_inline(inline_query):
  if len(inline_query.query) < 1:
    return
  answers = list()
  for i in range(10):
    styled_text = random_style_text(inline_query.query)
    ans_id = hashlib.md5(styled_text.encode("utf-8")).hexdigest()
    answers.append(types.InlineQueryResultArticle(ans_id, styled_text, types.InputTextMessageContent(styled_text, parse_mode="HTML")))
  bot.answer_inline_query(inline_query.id, answers)

bot.remove_webhook()
bot.polling(none_stop=True, interval=0, timeout=9999)
