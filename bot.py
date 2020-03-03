import telebot
import pyowm

owm = pyowm.OWM('63294dff63640c2518e4cfccb3fabcde', language="ru")
bot = telebot.TeleBot("1113301191:AAGiCwjps9e7waWM9ttxWBN2l1VuOQRDAoQ")

observation = owm.weather_at_place('place')
w = observation.get_weather()

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
