import os
import telebot
import logging
from config import *
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

# We guarantee that the server will start only with a direct call to the script __main__
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello! " + message.from_user)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(messange):
    bot.reply_to(messange, messange.text)


# Redirect from the Flask server to the bot
@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
