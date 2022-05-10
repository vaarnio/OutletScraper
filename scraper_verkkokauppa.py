""" 
A scraper should always return a dictionary with following key:value pairs:
    product - contains the product name
    price - outlet price
    normal_price - regular price
    outlet_store - the physical store where the item is located
    outlet_reason - for example the product could be a customer return or display piece
    outlet_id - unique identifier scraped from the outlet store api
"""

VERKKOKAUPPA_URLS = {
    "Base" : "http://www.verkkokauppa.com",
    "Search_request_all" : "https://web-api.service.verkkokauppa.com/search?pageSize=96&sort=releaseDate:desc&lang=fi&context=customer_returns_page",
    "Search_request_base" : "https://web-api.service.verkkokauppa.com/search?{0}pageNo=0&pageSize=48&sort=releaseDate:desc&lang=fi&context=customer_returns_page"
}


def construct_verkkokauppa_url(brands, categories):
    # 

    brand_filters = ""
    for brand in brands:
        brand = 'filter=brand:{0}&'.format(brand)
        brand_filters += brand

    category_filters = ""
    for category in categories:
        category = 'filter=category:{0}&'.format(category)
        category_filters += category

    url = VERKKOKAUPPA_URLS['Search_request_base'].format(brand_filters + category_filters)

    # constructed url example:
    # https://web-api.service.verkkokauppa.com/search?filter=category:22a&filter=brand:Apple&filter=brand:Asus&filter=brand:Belkin&userId=ec3676f4-9602-45f6-891f-d3fe18ab3304&rcs=eF5jYSlN9kg0MkkzSUo20jVJNDXVNTFKNtVNMra01DU0M01Jskw0sTBITeXKLSvJTOGztAAK6xoCAIyHDj0&sessionId=e38c2b53-d253-4ef6-8e05-ecc472df01d7&pageNo=0&pageSize=48&sort=releaseDate:desc&lang=fi&context=customer_returns_page
    return url.strip()


def scrape_verkkokauppa(session, brand, category):
    url = construct_verkkokauppa_url(brand, category)

    r = session.get(url)
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


if __name__ == "__main__":
    import sys
    from main import setup_session
    session = setup_session()
    print(scrape_verkkokauppa(session, [sys.argv[1]], [sys.argv[2]]))