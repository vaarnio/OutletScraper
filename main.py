from itertools import product
import requests
import random

import scrapers
import notifications
import product_helpers as p_hp
from user_agents import USER_AGENTS

def setup_session():
    session = requests.Session()
    session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
    return session

def main():
    session = setup_session()
    products = scrapers.scrape_power(session, ['Apple'], ['3341'])
    
    #create array containing only NEW products, THEN write ALL products to file
    new_products = p_hp.filter_old_products(products)
    p_hp.write_products_file(products)

    print('new products: \n')
    p_hp.print_products(new_products)
    for p in new_products:
        notifications.notify(p_hp.product_to_string(p))

if __name__ == "__main__":
    main()