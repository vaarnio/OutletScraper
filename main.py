import requests
import json
import random
import os
import scrapers
import notifications
from user_agents import USER_AGENTS
import sys

def product_to_string(p):
    return('Tuote: {0}\nHinta(outlet): {1}\nHinta(norm.): {2}\n{3}\n{4}\n'.format(
            p['product'], p['price'], p['normal_price'], p['outlet_store'], p['outlet_reason']))

def print_products(products):
    for p in products:
        product_text = product_to_string(p)
        print(product_text)

def read_data_file():
    try:
        with open('products.json', 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        try:
            #create file if it doesn't exist
            with open('products.json', 'x') as new_file:
                json.dump([], new_file)
        except Exception as e:
            print(e)
            sys.exit(1)

def write_data_file(data):
    try:
        with open('products.json', 'w') as outfile:
            json.dump(data, outfile)
    except Exception as e:
        print(e)

def compare_and_get_new(products):
    data = read_data_file()

    try:
        old_products = data['products']
    except:
        old_products = []
        write_data_file(old_products)

    old_product_ids = [p['outlet_id'] for p in old_products]
    #print(old_product_ids)
    for old_product in old_products:
        old_product_ids.append(old_product['outlet_id'])

    new_products = []
    for product in products:
        if product['outlet_id'] not in old_product_ids:
            new_products.append(product)

    return(new_products)

#scrape
session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
products = scrapers.scrape_power(session)

print_products(products)
for p in compare_and_get_new(products):
    notifications.notify(product_to_string(p))

write_data_file(products)

