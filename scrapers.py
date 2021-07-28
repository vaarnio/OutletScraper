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