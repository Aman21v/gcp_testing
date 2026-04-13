from flask import render_template, session, request, redirect, url_for
from . import frontend_bp

# Simulate calling other services by importing their functions
from project.product_service.routes import get_all_products, get_recommendations
from project.ad_service.routes import get_ads
# Assuming convert_currency is in project.services
from project.cart_service.routes import get_cart_from_session # Import cart helper
from project.services import convert_currency

@frontend_bp.route('/')
def home():
    """
    Home page route. It "calls" other services to get data.
    """
    ads = get_ads()
    recommended_products_raw = get_recommendations()
    target_currency = session.get('user_currency', 'USD') # Default to USD
    cart = get_cart_from_session() # Get current cart

    recommended_products_converted = {}
    if recommended_products_raw:
        for pid, product_details in recommended_products_raw.items():
            cart_quantity = cart.get(pid, 0) # Get quantity from cart, default to 0

            # Initialize with basic product details and cart quantity
            display_product = {
                **product_details, # spread all original details like name, price, currency etc.
                'cart_quantity': cart_quantity,
                'displayed_price': product_details.get('price'), # Default to original price
                'displayed_currency': product_details.get('currency') # Default to original currency
            }

            # Attempt to convert price if all necessary info is present
            if product_details and 'price' in product_details and 'currency' in product_details:
                original_price = product_details['price']
                original_currency = product_details['currency']
                converted_price = convert_currency(original_price, original_currency, target_currency)
                display_product['displayed_price'] = converted_price
                display_product['displayed_currency'] = target_currency
            
            recommended_products_converted[pid] = display_product

    return render_template('home.html', recommendations=recommended_products_converted, ads=ads, current_currency=target_currency)

@frontend_bp.route('/set_currency', methods=['POST'])
def set_currency():
    currency_code = request.form.get('currency')
    # Basic validation: ensure a currency was actually submitted and is supported (optional)
    supported_currencies = ['USD', 'EUR', 'INR'] # Example list
    if currency_code and currency_code in supported_currencies:
        session['user_currency'] = currency_code
    # Redirect back to the page the user was on, or home as a fallback
    return redirect(request.referrer or url_for('frontend.home'))

