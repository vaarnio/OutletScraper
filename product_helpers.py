import sys
import json

PRODUCTS_JSON = 'data/products.json'


#
# filter functions
#
def product_old_filter(product, old_product_ids):
    if(product['outlet_id'] in old_product_ids):
        return False
    else:
        return True


#
# product helpers
#
def product_to_string(p):
    return('Tuote: {0}\nHinta(outlet): {1}\nHinta(norm.): {2}\n{3}\n{4}\n'.format(
            p['product'], p['price'], p['normal_price'], p['outlet_store'], p['outlet_reason']))


def print_products(products):
    for p in products:
        product_text = product_to_string(p)
        print(product_text)


def filter_old_products(products):
    old_products = read_products_file()
    old_product_ids = [p['outlet_id'] for p in old_products]

    # filter function passed as lambda to allow second filter function argument
    # this way reading data_file each iteration can be avoided
    filtfunct = lambda product: product_old_filter(product, old_product_ids)
    new_products = list(filter(filtfunct, products))
    
    return(new_products)


#
# product file helpers
#
def read_products_file():
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


def write_products_file(data):
    try:
        with open(PRODUCTS_JSON, 'w') as outfile:
            json.dump(data, outfile, indent=4)
    except Exception as e:
        print(e)