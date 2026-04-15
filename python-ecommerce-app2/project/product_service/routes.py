from project.services import convert_currency

# Mock Product Data
MOCK_PRODUCTS = {
    'p001': {'name': 'Laptop', 'price': 1200, 'currency': 'USD'},
    'p002': {'name': 'Mouse', 'price': 25, 'currency': 'USD'},
    'p003': {'name': 'Keyboard', 'price': 75, 'currency': 'USD'},
    'p004': {'name': 'Monitor', 'price': 300, 'currency': 'INR'},
    'p005': {'name': 'headphones', 'price': 75, 'currency': 'USD'},
    'p006': {'name': 'mousepad', 'price': 300, 'currency': 'INR'},
}




# These functions simulate the service's API
def get_all_products():
    return MOCK_PRODUCTS

def get_product(product_id):
    return MOCK_PRODUCTS.get(product_id)

def get_recommendations():
    # In a real app, this would have complex logic.
    # Here, it "calls" its own product catalog.
    products = get_all_products()
    return {pid: p for pid, p in products.items() if pid in ['p001', 'p002', 'p003', 'p004','p005','p006']}
    
def get_product_for_display(product_id, target_currency):
    """
    Gets product details and converts its price to the target_currency.
    Uses the convert_currency function from services.py.
    """
    product = MOCK_PRODUCTS.get(product_id)
    if not product:
        return None

    original_price = product['price']
    original_currency = product['currency']

    if original_currency == target_currency:
        displayed_price = original_price
    else:
        displayed_price = convert_currency(original_price, original_currency, target_currency)
    
    return {
        **product, # Original product details
        'displayed_price': displayed_price,
        'displayed_currency': target_currency 
    }
