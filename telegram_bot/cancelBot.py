from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import json
import datetime

URL_SERVER_CANCEL = 'http://localhost:3333/cancel'

#Get token
token = None
try:
    file_key = open('token.txt', 'r')
    token = file_key.readline()
    file_key.close()
except:
    print("FILE DOESN'T EXIST, ANYTHING WILL HAPPEN")


updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

#start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="KKKKKKKK eu sou.......\nUm bot?")

#cancel_list command
def see_cancel(update, context):

    #getting list from server
    response = requests.get(URL_SERVER_CANCEL)
    lista = response.json()
    
    #Making a message for each item from the response
    for item in lista:
        id_cancel = item['id']
        user = item['user']
        app = item['app']
        time = item['time']

        message = "item: " + str(id_cancel) + "\nuser: " + user + "\nwhere: " + app + "\nwhen: " + time

        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

#new_cancel command
def new_cancel(update, context):

    #getting username and data
    user = update.message.from_user.username

    currentDT = datetime.datetime.now()
    day = currentDT.day
    month = currentDT.month
    year = currentDT.year
    hour = currentDT.hour
    minute = currentDT.minute

    #converting data for a new format
    time = str(day) + '/' + str(month) + '/' + str(year) + ' - ' + str(hour) + 'h' + str(minute)

    #sending infos to server
    data = {'user':user, 'app':'telegram', 'time':time}
    r = requests.post(URL_SERVER_CANCEL, json=data)
    context.bot.send_message(chat_id=update.effective_chat.id, text='@PedroEsnaola says "a"')


#creating handlers and commands
start_handler = CommandHandler('start', start)
cancelled_handler = CommandHandler('cancel_list', see_cancel)
new_cancel_handler = CommandHandler('new_cancel', new_cancel)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(cancelled_handler)
dispatcher.add_handler(new_cancel_handler)

updater.start_polling()

