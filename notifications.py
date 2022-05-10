import telegram
import os
import sys
import json


#set bot token in enrionmental variable 'outlet_bot_token' before using
TOKEN = os.environ.get('outlet_bot_token')
BOT = telegram.Bot(token=TOKEN)
CHAT_IDS_PATHNAME = 'chat_ids.json'

def read_chat_ids(pathname):
    try:
        with open(pathname, 'r') as json_file:
            data = json.load(json_file)
            return data 
    except FileNotFoundError:
        try:
            #create file if it doesn't exist
            with open(pathname, 'x') as new_file:
                json.dump([], new_file)
        except Exception as e:
            print(e)
            sys.exit(1)
       

def write_chat_ids(data, pathname):
    try:
        with open(pathname, 'w') as outfile:
            json.dump(data, outfile)
    except Exception as e:
        print(e)
        sys.exit(1)


def update_chat_ids():
    # adds new telegram chat subscribers to CHAT_IDS_PATHNAME
    # also returns a list containing all subscribers.

    #get new subscribers from telegram api
    updates = BOT.get_updates()
    new_chat_ids = [c.message.from_user.id for c in updates]
    new_chat_ids = list(set(new_chat_ids)) #remove duplicates by converting to set and back to list

    #get old subscribers from file
    try:
        chat_ids = read_chat_ids(CHAT_IDS_PATHNAME)
        new_chat_ids = [chat for chat in new_chat_ids if chat not in chat_ids]
        print('New telegram bot chat ids: {0}'.format(new_chat_ids))
        chat_ids += new_chat_ids
    except:
        chat_ids = new_chat_ids

    write_chat_ids(chat_ids, CHAT_IDS_PATHNAME)
    return chat_ids


def send_telegram_message(message):
    chat_ids = update_chat_ids()

    print('Sending a message to following chats: {0}'.format(chat_ids))
    for c_id in chat_ids:
        try:
            BOT.send_message(text=message, chat_id=c_id)
        except telegram.error.BadRequest:
            print('Could not send message to: {0}'.format(c_id))
            chat_ids.remove(c_id)
            write_chat_ids(chat_ids)


def notify(message):
    # method to send message on all available notification daemons
    send_telegram_message(message)


if __name__ == "__main__":
    import sys
    notify(sys.argv[1])