import requests
import random

import scrapers
from user_agents import USER_AGENTS

#scrape
print('starting scraping')
session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
products = scrapers.scrape_power(session)
print('scraping complete')