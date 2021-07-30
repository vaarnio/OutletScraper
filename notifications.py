import telegram
import os
import sys
import json

def read_chat_ids():
    try:
        with open('chat_ids.json', 'r') as json_file:
            data = json.load(json_file)
            return data 
    except FileNotFoundError:
        try:
            #create file if it doesn't exist
            with open('chat_ids.json', 'x') as new_file:
                json.dump([], new_file)
        except Exception as e:
            print(e)
            sys.exit(1)
       
def write_data_file(data):
    try:
        with open('chat_ids.json', 'w') as outfile:
            json.dump(data, outfile)
    except Exception as e:
        print(e)
        sys.exit(1)

def send_telegram_message(message):
    #set bot token in enrionmental variable 'outlet_bot_token' before using
    token = os.environ.get('outlet_bot_token')
    bot = telegram.Bot(token=token)

    #get new subscribers from telegram api
    updates = bot.get_updates()
    print(updates)
    new_chat_ids = [c.message.from_user.id for c in updates]
    new_chat_ids = list(set(new_chat_ids)) #remove duplicates by converting to set and back to list

    #get old subscribers from file
    data = read_chat_ids()
    try:
        chat_ids = data
        new_chat_ids = [chat for chat in new_chat_ids if chat not in chat_ids]
        print('New telegram bot chat ids: {0}'.format(new_chat_ids))
        chat_ids += new_chat_ids
    except:
        chat_ids = new_chat_ids
    write_data_file(chat_ids)

    print('Sending a message to following chats: {0}'.format(chat_ids))
    for c_id in chat_ids:
        try:
            bot.send_message(text=message, chat_id=c_id)
        except telegram.error.BadRequest:
            print('Could not send message to: {0}'.format(c_id))
            chat_ids.remove(c_id)
    write_data_file(chat_ids)

def notify(message):
    send_telegram_message(message)