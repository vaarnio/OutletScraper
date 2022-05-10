import requests
import random

import scrapers
import notifications
import product_helpers as p_hp
from user_agents import USER_AGENTS

#scrape
print('starting scraping')
session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
products = scrapers.scrape_power(session, ['Apple'], ['3341'])
print('scraping done')

#create array containin only NEW products, THEN write ALL products to file
new_products = p_hp.filter_old_products(products)
p_hp.write_products_file(products)

print('new products: \n')
p_hp.print_products(new_products)
for p in new_products:
    notifications.notify(p_hp.product_to_string(p))



