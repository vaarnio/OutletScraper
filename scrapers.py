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
    # store number: 0
    "Base" : "http://www.power.fi",
    "Search_request_all" : "https://www.power.fi/umbraco/api/product/getproductsbysearchrequest?from=0&o=true&q=outlet&s=5&size=36",
    "Search_request_base" : "http://www.power.fi/umbraco/api/product/getproductsbysearchrequest?{0}from=0&o=true&q=outlet&s=5&size=36",
    "Brand_base" : "f-1-BasicBrand={0}&",
    "Category_base" : "f-1-BasicCategories={0}&",
}

VERKKOKAUPPA_URLS = {
    # store number: 1
    "Base" : "http://www.verkkokauppa.com",
    "Search_request_all" : "https://web-api.service.verkkokauppa.com/search?pageSize=96&sort=releaseDate:desc&lang=fi&context=customer_returns_page",
    "Search_request_base" : "https://web-api.service.verkkokauppa.com/search?{0}pageNo=0&pageSize=48&sort=releaseDate:desc&lang=fi&context=customer_returns_page",
    "Brand_base" : "filter=brand:{0}&",
    "Category_base" : "filter=category:{0}&",
}


def construct_url(brands, categories, store_urls):
    # available brands and categories are listed in filters/brandFilters.json and filters/categoryFilters.json

    brand_filters = ""
    for brand in brands:
        brand = store_urls['Brand_base'].format(brand)
        brand_filters += brand

    category_filters = ""
    for category in categories:
        category = store_urls['Category_base'].format(category)
        category_filters += category

    url = store_urls["Search_request_base"].format(brand_filters + category_filters)

    # constructed url example:
    # https://web-api.service.verkkokauppa.com/search?filter=category:22a&filter=brand:Apple&filter=brand:Asus&filter=brand:Belkin&userId=ec3676f4-9602-45f6-891f-d3fe18ab3304&rcs=eF5jYSlN9kg0MkkzSUo20jVJNDXVNTFKNtVNMra01DU0M01Jskw0sTBITeXKLSvJTOGztAAK6xoCAIyHDj0&sessionId=e38c2b53-d253-4ef6-8e05-ecc472df01d7&pageNo=0&pageSize=48&sort=releaseDate:desc&lang=fi&context=customer_returns_page
    return url.strip()


def scrape_power(session, outlet_query_url):
    r = session.get(outlet_query_url)
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


def scrape_verkkokauppa(session, outlet_query_url):
    r = session.get(outlet_query_url)
    json = r.json()
    products = []
    for p in json['products']:
        customer_returns_info = p['customerReturnsInfo']
        products.append({
            'product': customer_returns_info['product_name'],
            'price': customer_returns_info['price_with_tax'],
            'normal_price': p['price']['current'],
            'outlet_store': "Verkkokauppa.com",
            'outlet_reason': customer_returns_info['product_extra_info'],
            'outlet_id' : customer_returns_info['id'],
            'product_url' : VERKKOKAUPPA_URLS['Base'] + '/fi/outlet/yksittaiskappaleet/{0}'.format(customer_returns_info['id'])
        })

    return products

def scrape(session, brands, categories, store_num):
    if(store_num == '1'):
        outlet_query_url = construct_url(brands, categories, VERKKOKAUPPA_URLS)
        return scrape_verkkokauppa(session, outlet_query_url)
    elif(store_num == '0'):
        outlet_query_url = construct_url(brands, categories, POWER_URLS)
        return scrape_power(session, outlet_query_url)
    else:
        raise ValueError('Store number invalid: ', store_num)


if __name__ == "__main__":
    import sys
    from main import setup_session
    session = setup_session()
    print(scrape(session, [sys.argv[1]], [sys.argv[2]], sys.argv[3]))