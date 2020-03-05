import telebot
import pyowm
import flask
from telebot import types
from config import *
from igornotrobot import bot
import os
 
server = flask.Flask(__name__)
 
 
@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(
         flask.request.stream.read().decode("utf-8"))])
    return "!", 200
 
 
@server.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
    return "Hello from Heroku!", 200
 
 
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

owm = pyowm.OWM('63294dff63640c2518e4cfccb3fabcde', language="ru")
bot = telebot.TeleBot("1113301191:AAGiCwjps9e7waWM9ttxWBN2l1VuOQRDAoQ")

@bot.message_handler(content_types=['text'])
def send_echo(message):
    observation = owm.weather_at_place(message.text)
    w = observation.get_weather()
    temp = w.get_temperature('celsius')['temp']

    answer = "В городе " + message.text + " сейчас " + w.get_detailed_status() +"\n"
    answer += 'Температура в районе ' + str(temp) + "\n\n"

    if temp < 10:
        answer += 'Ппц как холодно, надень всё что у тебя есть!'
    elif temp < 20:
        answer += 'Прохладно, оденься потеплее' 
    else:
        answer += "Температура ок, одевай что угодно и го флексить." 
        
    bot.send_message(message.chat.id, answer)

bot.polling( none_stop = True )
