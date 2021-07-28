""" 
A scraper should always return a dictionary with following key:value pairs:
    product - contains the product name
    price - outlet price
    normal_price - regular price
    outlet_store - the physical store where the item is located
    outlet_reason - for example the product could be a customer return or display piece
    outlet_id - unique identifier scraped from the outlet store api

Try to scrape all the needed information, do not generate information in the scraper method.
"""

STORE_URLS = {
    "Power": "http://www.power.fi/umbraco/api/product/getproductsbysearchrequest?f-1-BasicBrand=Apple&f-1-BasicCategories=3341&from=0&o=true&q=outlet&s=5&size=36"
}

def scrape_power(session):
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