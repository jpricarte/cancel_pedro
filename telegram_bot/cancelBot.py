from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import json
import datetime
import random

#Server's url
URL_SERVER_CANCEL = 'http://localhost:3333/cancel'
#seed the random class
random.seed(datetime.time)


'''
    Some things to make pedro_cancel_bot work
'''
#Get token
token = None
try:
    file_key = open('token.txt', 'r')
    token = file_key.readline()
    file_key.close()
except:
    print("FILE DOESN'T EXIST, ANYTHING WILL HAPPEN")

#inicializing updater and dispatcher
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


'''
    Auxiliar functions
'''
def convert_time(timestamp):
    '''
        Convert timestamp to brazilian view of time
    '''
    item_dt = datetime.datetime.fromtimestamp(timestamp)

    #converting data for a new format
    day = item_dt.day
    month = item_dt.month
    year = item_dt.year
    hour = item_dt.hour
    minute = item_dt.minute
    time_converted = str(day) + '/' + str(month) + '/' + str(year) + ' - ' + str(hour) + 'h' + str(minute)

    return time_converted


def create_message(cancel):
    '''
        create the infos about some cancel
    '''
    id_cancel = cancel['id']
    user = cancel['user']
    app = cancel['app']
    timestamp = int(cancel['time'])
        
    time = convert_time(timestamp)
        
    message = "item: " + str(id_cancel) + "\nuser: " + user + "\nwhere: " + app + "\nwhen: " + time
    return message


'''
    Commands functions
'''
#start command
def start(update, context):
    '''
        Send start's bot info
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text="KKKKKKKK eu sou.......\nUm bot?")

#cancel_list command
def cancel_list(update, context):
    '''
        List all cancels
    '''
    #getting list from server
    response = requests.get(URL_SERVER_CANCEL)
    lista = response.json()
    
    #Making a message for each item from the response
    for item in lista:
        message = create_message(item)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def last_cancel(update, context):
    '''
        Show last cancel
    '''
    #getting list from server
    response = requests.get(URL_SERVER_CANCEL)
    lista = response.json()
    #taking last ellement
    last_cancel = lista[-1]

    infos = create_message(last_cancel)    
    message = "Pedro's last cancellation\n" + infos

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

#new_cancel command
def new_cancel(update, context):
    '''
        Register a new cancel
    '''
    #getting username and data
    user = update.message.from_user.username
    if user == None:
        user = 'Algum arrombado sem user'

    current_dt = int(datetime.datetime.now().timestamp())
    
    #sending infos to server
    data = {'user':user, 'app':'telegram', 'time':current_dt}
    r = requests.post(URL_SERVER_CANCEL, json=data)
    context.bot.send_message(chat_id=update.effective_chat.id, text='@PedroEsnaola says "a"')


def felt_guilty(update, context):
    random_line = None
    with open('frases.txt', 'r') as archive:
        lines = archive.read().splitlines()
        random_line = random.choice(lines)
        archive.close()
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=random_line)

'''
    Creating all handlers
'''
start_handler = CommandHandler('start', start)
cancelled_handler = CommandHandler('cancel_list', cancel_list)
last_cancel_handler = CommandHandler('last_cancel', last_cancel)
new_cancel_handler = CommandHandler('new_cancel', new_cancel)
felt_guilty_handler = CommandHandler('felt_guilty', felt_guilty)


'''
    Adding handlers to dispatcher
'''
dispatcher.add_handler(start_handler)
dispatcher.add_handler(cancelled_handler)
dispatcher.add_handler(last_cancel_handler)
dispatcher.add_handler(new_cancel_handler)
dispatcher.add_handler(felt_guilty_handler)


'''
    Starting bot
'''
updater.start_polling()