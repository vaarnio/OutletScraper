import telegram
import os
import sys
import json


#set bot token in enrionmental variable 'outlet_bot_token' before using
TOKEN = os.environ.get('outlet_bot_token')
BOT = telegram.Bot(token=TOKEN)
CHAT_IDS_PATHNAME = 'data/chat_ids.json'

class NotificationService:

    def __init__(self):
        self.chat_ids = self.update_chat_ids()

    @staticmethod
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
    
    @staticmethod
    def write_chat_ids(data, pathname):
        try:
            with open(pathname, 'w') as outfile:
                json.dump(data, outfile)
        except Exception as e:
            print(e)
            sys.exit(1)


    def update_chat_ids(self):
        # adds new telegram chat subscribers to CHAT_IDS_PATHNAME
        # also returns a list containing all subscribers.

        #get new subscribers from telegram api
        updates = BOT.get_updates()
        new_chat_ids = [c.message.from_user.id for c in updates]
        new_chat_ids = list(set(new_chat_ids)) #remove duplicates by converting to set and back to list

        #get old subscribers from file
        try:
            self.chat_ids = self.read_chat_ids(CHAT_IDS_PATHNAME)
            new_chat_ids = [chat for chat in new_chat_ids if chat not in self.chat_ids]
            print('New telegram bot chat ids: {0}'.format(new_chat_ids))
            self.chat_ids += new_chat_ids
        except:
            self.chat_ids = new_chat_ids

        self.write_chat_ids(self.chat_ids, CHAT_IDS_PATHNAME)
        return self.chat_ids


    def send_telegram_message(self, message):
        print('Sending a message to following chats: {0}'.format(self.chat_ids))
        for c_id in self.chat_ids:
            try:
                BOT.send_message(text=message, chat_id=c_id, timeout=1000)
            except telegram.error.BadRequest:
                print('Could not send message to: {0}'.format(c_id))
                self.chat_ids.remove(c_id)
                self.write_chat_ids(self.chat_ids)


    def notify(self, message):
        # method to send message on all available notification daemons
        self.send_telegram_message(message)


if __name__ == "__main__":
    import sys
    notif_serv = NotificationService()
    notif_serv.notify(sys.argv[1])