import random
import requests

import scrapers
from notifications import NotificationService
import product_helpers as p_hp
from user_agents import USER_AGENTS

def setup_session():
    session = requests.Session()
    session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
    return session

def main():
    session = setup_session()
    products = scrapers.scrape(session, ['Apple'], ['3341'], '0')

    #create array containing only NEW products, THEN write ALL products to file
    new_products = p_hp.filter_old_products(products)
    p_hp.write_products_file(products)

    if(len(new_products) > 0):
        print('new products: \n')
        p_hp.print_products(new_products)

        notif_serv = NotificationService()
        for product in new_products:
            notif_serv.notify(p_hp.product_to_string(product))

if __name__ == "__main__":
    main()