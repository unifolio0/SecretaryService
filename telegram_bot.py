from SecretaryService import *
from account import *
import telegram
from telegram.ext import Updater, CommandHandler

def telegram_msg():
    bot = telegram.Bot(token=MY_TOKEN)
    chat_id = CHAT_ID
    content = set_content()
    bot.sendMessage(chat_id=chat_id, text=content)

token = MY_TOKEN

updater = Updater(token=token)
dispatcher = updater.dispatcher

def weather(update, context):  # 오늘의 날씨 보내기
  context.bot.send_message(chat_id=update.effective_chat.id, text=today_weather())

weather_handler = CommandHandler('weather', weather)
dispatcher.add_handler(weather_handler)

def politics(update, context):  # 정치기사 5개 보내기
  context.bot.send_message(chat_id=update.effective_chat.id, text=today_politics())

politics_handler = CommandHandler('politics', politics)
dispatcher.add_handler(politics_handler)

def business(update, context):  # 경제기사 5개 보내기
  context.bot.send_message(chat_id=update.effective_chat.id, text=today_business())

business_handler = CommandHandler('business', business)
dispatcher.add_handler(business_handler)

def itscience(update, context):  # IT/과학기사 5개 보내기
  context.bot.send_message(chat_id=update.effective_chat.id, text=today_it_science())

itscience_handler = CommandHandler('itscience', itscience)
dispatcher.add_handler(itscience_handler)

updater.start_polling()
updater.idle()