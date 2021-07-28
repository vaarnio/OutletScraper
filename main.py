import requests
import json
import random
import telegram
import os
import scrapers
from user_agents import USER_AGENTS

def product_to_string(p):
    return('Tuote: {0}\nHinta(outlet): {1}\nHinta(norm.): {2}\n{3}\n{4}\n'.format(
            p['product'], p['price'], p['normal_price'], p['outlet_store'], p['outlet_reason']))

def print_products(products):
    for p in products:
        product_text = product_to_string(p)
        print(product_text)

def read_data_file():
    try:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(e)
        data = {}
        write_data_file(data)
    finally:
        return data 

def write_data_file(data):
    try:
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    except Exception as e:
        print(e)


def add_array_to_data_file(pair_name, data_array):
    data = read_data_file()
    data[pair_name] = []
    [data[pair_name].append(p) for p in data_array if p not in data[pair_name]]

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def compare_and_get_new(products):
    data = read_data_file()

    try:
        old_products = data['products']
    except:
        old_products = []
        add_array_to_data_file('products', old_products)

    old_product_ids = [p['outlet_id'] for p in old_products]
    #print(old_product_ids)
    for old_product in old_products:
        old_product_ids.append(old_product['outlet_id'])

    new_products = []
    for product in products:
        if product['outlet_id'] not in old_product_ids:
            new_products.append(product)

    return(new_products)

def send_telegram_message(message):
    #set bot token in enrionmental variable 'outlet_bot_token' before using
    token = os.environ.get('outlet_bot_token')
    bot = telegram.Bot(token=token)

    #get new subscribers from telegram api
    updates = bot.get_updates()
    new_chat_ids = [c.message.from_user.id for c in updates]
    new_chat_ids = list(set(new_chat_ids)) #remove duplicates by converting to set and back to list

    #get old subscribers from file
    data = read_data_file()
    try:
        chat_ids = data['chats']
        new_chat_ids = [chat for chat in new_chat_ids if chat not in chat_ids]
        print('New telegram bot chat ids: {0}'.format(new_chat_ids))
        chat_ids += new_chat_ids
    except:
        chat_ids = new_chat_ids
    finally:
        add_array_to_data_file('chats', chat_ids)

    print('Sending message to following chats: {0}'.format(chat_ids))
    for c_id in chat_ids:
        bot.send_message(text=message, chat_id=c_id)

#scrape
session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
products = scrapers.scrape_power(session)

print_products(products)
""" for p in compare_and_get_new(products):
    send_telegram_message(product_to_string(p))

add_array_to_data_file('products', products) """

