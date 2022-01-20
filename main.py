import os
import telebot
from telebot import types
import logging
import psycopg2
from config import *
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()


def update_messages_count(user_id):
    db_object.execute(f"UPDATE users SET messanges = messanges + 1 WHERE id = {user_id}")
    db_connection.commit()


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    day_button = types.KeyboardButton("Дни недели")
    group_button = types.KeyboardButton("Группы")
    discipline_button = types.KeyboardButton("Предметы")
    auditory_button = types.KeyboardButton("Аудитории")
    pair_button = types.KeyboardButton("Пары")
    users_data = types.KeyboardButton("Данные пользователя")
    markup.add(day_button, group_button, discipline_button, auditory_button, pair_button, users_data)
    user_id = message.from_user.id
    username = message.from_user.username
    bot.reply_to(message, f"Hello, {username}!", reply_markup=markup)

    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id, username, messanges) VALUES (%s, %s, %s)", (user_id, username, 0))
        db_connection.commit()

    update_messages_count(user_id)





@bot.message_handler(commands=["day"])
def get_week_days(message):
    chat_id = message.chat.id
    db_object.execute(f"SELECT * FROM day")
    the_day = db_object.fetchall()
    for row in the_day:
        bot.send_message(chat_id, row[1])

    update_messages_count(message.from_user.id)


@bot.message_handler(commands=["stats"])
def get_stats(message):
    db_object.execute("SELECT * FROM users ORDER BY messanges DESC LIMIT 10")
    result = db_object.fetchall()

    if not result:
        bot.reply_to(message, "No data...")
    else:
        reply_message = "users db:\n"
        for i, item in enumerate(result):
            reply_message += f"{item[1].strip()} id({item[0]}) group({item[3]}) : {item[2]} messages.\n"
        bot.reply_to(message, reply_message)

    update_messages_count(message.from_user.id)


@bot.message_handler(content_types=["text"])
def bot_menu(message):
    if message.text == "Дни недели":
        get_week_days(message)
    elif message.text == "Данные пользователя":
        bot.send_message(message.chat.id, "В процессе разработки")
    elif message.text == "Группы":
        bot.send_message(message.chat.id, "В процессе разработки")
    elif message.text == "Предметы":
        bot.send_message(message.chat.id, "В процессе разработки")
    elif message.text == "Аудитории":
        bot.send_message(message.chat.id, "В процессе разработки")
    elif message.text == "Пары":
        bot.send_message(message.chat.id, "В процессе разработки")

    update_messages_count(message.from_user.id)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_from_user(message):
    user_id = message.from_user.id
    update_messages_count(user_id)


@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

##################################################################
# @bot.message_handler(commands=["stats"])
# def get_stats(message):
#     db_object.execute("SELECT * FROM users ORDER BY messanges DESC LIMIT 10")
#     result = db_object.fetchall()
#
#     if not result:
#         bot.reply_to(message, "No data...")
#     else:
#         reply_message = "- Top flooders:\n"
#         for i, item in enumerate(result):
#             reply_message += f"[{i + 1}] {item[1].strip()} ({item[0]}) : {item[2]} messages.\n"
#         bot.reply_to(message, reply_message)
#
#     update_messages_count(message.from_user.id)


# @bot.message_handler(content_types=["text"])
# def bot_menu(message):
#     if message.text == "Дни недели":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         back = types.KeyboardButton("Назад")
#         markup.add(back)
#         get_week_days()
#     elif message.text == "Назад":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         day_buttton = types.KeyboardButton("Дни недели")
#         markup.add(day_buttton)
#         bot.reply_to(message, "Назад", reply_markup=markup)
#
#     update_messages_count(message.from_user.id)