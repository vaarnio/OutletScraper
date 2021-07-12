import requests
import json
import random
from user_agents import USER_AGENTS
from store_urls import STORE_URLS

def scraper_power(session):
    r = session.get(STORE_URLS['Power'])
    json = r.json()

    data = []
    for p in json['Products']:
        data.append({
            'product': p['SearchTitle'],
            'price': p['Price'],
            'normal_price': p['OutletProductNormalPrice'],
            'outlet_store': p['OutletStore'],
            'outlet_reason': p['OutletReason'],
            'outlet_id' : p['OutletId']
        })
    return data

def product_to_string(p):
    return('Tuote: {0}\nHinta(outlet): {1}\nHinta(norm.): {2}\n{3}\n{4}\n'.format(
            p['product'], p['price'], p['normal_price'], p['outlet_store'], p['outlet_reason']))

def print_products(products):
    for p in products:
        product_text = product_to_string(p)
        print(product_text)

def json_to_file(products):
    data = {}
    data['products'] = []
    [data['products'].append(p) for p in products]

    with open('products.json', 'w') as outfile:
        json.dump(data, outfile)

def test(session):
    return("testi")

def compare_and_get_new(products):
    try:
        with open('products.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(e)
        return([])

    old_products = data['products']

    old_product_ids = [p['outlet_id'] for p in old_products]
    print(old_product_ids)
    for old_product in old_products:
        old_product_ids.append(old_product['outlet_id'])

    new_products = []
    for product in products:
        if product['outlet_id'] not in old_product_ids:
            new_products.append(product)

    return(new_products)


session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
products = []

products += scraper_power(session)
print_products(products)
print(compare_and_get_new(products))
json_to_file(products)