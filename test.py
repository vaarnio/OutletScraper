import requests
import random

import scrapers
from user_agents import USER_AGENTS

def create_session():
    session = requests.Session()
    session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
    return session

#scrape
print('starting test')

session = create_session()
products = scrapers.scrape_power(session, ['Apple', 'Huawei'], ['3341'])
#products = scrapers.scrape_filters(session)
#products = scrapers.constructUrl(['Apple', 'Huawei'], ['3341'])

print(products)

print('test complete')