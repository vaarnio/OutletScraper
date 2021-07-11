import requests
import json
import random
import sqlite3
from sqlite3 import Error
from user_agents import USER_AGENTS
from store_urls import STORE_URLS
from db import Db


def scraper_power(session):
    r = session.get(STORE_URLS['Power'])
    json = r.json()

    products = []
    for p in json['Products']:
        products.append({
            'product': p['SearchTitle'],
            'price': p['Price'],
            'normal_price': p['OutletProductNormalPrice'],
            'outlet_store': p['OutletStore'],
            'outlet_reason': p['OutletReason']
        })
    return products


def print_products(products):
    for p in products:
        product_text = 'Tuote: {0}\nHinta(outlet): {1}\nHinta(norm.): {2}\n{3}\n{4}\n'.format(p['product'], p['price'], p['normal_price'], p['outlet_store'], p['outlet_reason'])
        print(product_text)


def test(session):
    return("testi")


db = Db('products.db')
session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
products = []

#products += scraper_power(session)
print_products(products)