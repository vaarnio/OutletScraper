import requests
import json
import random
import os
import sys

import scrapers
import notifications
from user_agents import USER_AGENTS

PRODUCTS_JSON = 'products.json'

def product_to_string(p):
    return('Tuote: {0}\nHinta(outlet): {1}\nHinta(norm.): {2}\n{3}\n{4}\n'.format(
            p['product'], p['price'], p['normal_price'], p['outlet_store'], p['outlet_reason']))

def print_products(products):
    for p in products:
        product_text = product_to_string(p)
        print(product_text)

def read_data_file():
    try:
        with open(PRODUCTS_JSON, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        try:
            #create file if it doesn't exist
            with open(PRODUCTS_JSON, 'x') as new_file:
                json.dump([], new_file)
                return []
        except Exception as e:
            print(e)
            sys.exit(1)

def write_data_file(data):
    try:
        with open(PRODUCTS_JSON, 'w') as outfile:
            json.dump(data, outfile)
    except Exception as e:
        print(e)

def product_old_filter(product, old_product_ids):
    if(product['outlet_id'] in old_product_ids):
        return False
    else:
        return True

def filter_products(products):
    old_products = read_data_file()
    old_product_ids = [p['outlet_id'] for p in old_products]

    # filter function passed as lambda to allow second filter function argument
    # this way reading data_file each iteration can be avoided
    filtfunct = lambda product: product_old_filter(product, old_product_ids)
    new_products = list(filter(filtfunct, products))
    
    return(new_products)

#scrape
print('starting scraping')
session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
products = scrapers.scrape_power(session, ['Apple'], ['3341'])
print('scraping complete')

#create array containin only NEW products, THEN write ALL products to file
new_products = filter_products(products)
write_data_file(products)

print('new products: \n')
print_products(new_products)
for p in new_products:
    notifications.notify(product_to_string(p))



