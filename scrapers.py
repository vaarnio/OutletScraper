""" 
A scraper should always return a dictionary with following key:value pairs:
    product - contains the product name
    price - outlet price
    normal_price - regular price
    outlet_store - the physical store where the item is located
    outlet_reason - for example the product could be a customer return or display piece
    outlet_id - unique identifier scraped from the outlet store api
"""

POWER_URLS = {
    "Base" : "http://www.power.fi",
    "Search_request_all" : "https://www.power.fi/umbraco/api/product/getproductsbysearchrequest?from=0&o=true&q=outlet&s=5&size=36",
    "Search_request_base" : "http://www.power.fi/umbraco/api/product/getproductsbysearchrequest?{0}from=0&o=true&q=outlet&s=5&size=36"
}


def construct_url(brands, categories):
    # available brands and categories are listed in JSON/brandFilters.json and JSON/categoryFilters.json

    brand_filters = ""
    for brand in brands:
        brand = 'f-1-BasicBrand={0}&'.format(brand)
        brand_filters += brand

    category_filters = ""
    for category in categories:
        category = 'f-1-BasicCategories={0}&'.format(category)
        category_filters += category

    url = POWER_URLS['Search_request_base'].format(brand_filters + category_filters)

    # constructed url example:
    # https://www.power.fi/umbraco/api/product/getproductsbysearchrequest?f-1-BasicBrand=HP&f-1-BasicBrand=Honor&f-1-BasicBrand=Huawei&from=0&o=true&q=outlet&s=5&size=36
    return url.strip()


def scrape_power(session, brand, category):
    url = construct_url(brand, category)
    
    r = session.get(url)
    json = r.json()

    products = []
    for p in json['Products']:
        products.append({
            'product': p['SearchTitle'],
            'price': p['Price'],
            'normal_price': p['OutletProductNormalPrice'],
            'outlet_store': p['OutletStore'],
            'outlet_reason': p['OutletReason'],
            'outlet_id' : p['OutletId'],
            'product_url' : POWER_URLS["Base"] + p['Url']
        })
    return products