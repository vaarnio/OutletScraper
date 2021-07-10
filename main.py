import requests
import json
import random
from user_agents import USER_AGENTS
from store_urls import STORE_URLS

def scraper_power(session):
    r = session.get(STORE_URLS['Power'])
    json = r.json()
    #products = json.dumps(json['Products'], sort_keys=True, indent=4)

    print(r.headers)

    for p in json['Products']:
        product_text = 'Tuote: {0}\nHinta(ale)): {1}\nHinta(norm.): {2}\n{3}\n'.format(p['SearchTitle'], p['Price'], p['OutletProductNormalPrice'], p['OutletReason'])
        print(product_text)

session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})

scraper_power(session)