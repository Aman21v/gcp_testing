from flask import request, redirect, url_for, session, render_template
from . import cart_bp
from project.product_service.routes import get_product, get_product_for_display
from project.services import convert_currency, get_shipping_quote # Import get_shipping_quote

def get_cart_from_session():
    """
    Helper function to safely get the cart dictionary from the session.
    It returns an empty dictionary if the cart doesn't exist yet.
    """
    return session.get('cart', {})

@cart_bp.route('/cart', methods=['GET'])
def view_cart():
    # Get the entire cart dictionary directly from the session.
    cart_items_raw = get_cart_from_session()
    target_currency = session.get('user_currency', 'USD') # Get target currency

    cart_items_display = []
    items_total_converted = 0 # This will be the subtotal for items only

    # Loop through the dictionary items (product_id: quantity)
    for product_id, quantity in cart_items_raw.items():
        # "Call" the product service to get details
        product_info = get_product(product_id)
        if product_info:
            original_price = product_info['price']
            original_currency = product_info['currency']

            # Convert individual item price to the target currency
            displayed_item_price = convert_currency(original_price, original_currency, target_currency)
            
            # Calculate item total in the target currency
            item_total_converted = displayed_item_price * quantity
            items_total_converted += item_total_converted # Accumulate item totals
            
            cart_items_display.append({
                'id': product_id,
                'name': product_info['name'],
                'quantity': quantity,
                'price_original': original_price, # Store original price for reference
                'currency_original': original_currency, # Store original currency
                'price_displayed': displayed_item_price, # Price per unit in target currency
                'item_total_displayed': item_total_converted, # Total for this line item in target currency
                'currency_displayed': target_currency # The currency prices are displayed in
            })

    displayed_shipping_cost = None
    if session.get('shipping_calculated_for_cart'): # Check if shipping has been calculated
        raw_shipping_usd = session.get('cart_shipping_quote_raw_usd', 0)
        if raw_shipping_usd > 0: # Only process if there's an actual cost
            displayed_shipping_cost = convert_currency(raw_shipping_usd, 'USD', target_currency)

    grand_total_displayed = items_total_converted
    if displayed_shipping_cost is not None:
        grand_total_displayed += displayed_shipping_cost
            
    return render_template('cart.html', 
                           cart_items=cart_items_display, 
                           items_total_displayed=items_total_converted, # Pass subtotal
                           displayed_shipping_cost=displayed_shipping_cost, # Pass shipping cost
                           grand_total_displayed=grand_total_displayed, # Pass final grand total
                           current_currency=target_currency)

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))

    if product_id:
        # Get a mutable copy of the cart from the session
        cart = get_cart_from_session()
        
        # Update the quantity in the dictionary
        current_quantity = cart.get(product_id, 0)
        cart[product_id] = current_quantity + quantity
        
        # Save the updated cart dictionary back into the session
        session['cart'] = cart
        # Clear previously calculated shipping cost as cart has changed
        session.pop('shipping_calculated_for_cart', None)
        session.pop('cart_shipping_quote_raw_usd', None)

    return redirect(url_for('cart.view_cart'))

# Note: This route for product details is currently in the cart_service.
# It might be more logically placed in the product_service.
# If cart_bp has a URL prefix (e.g., '/cart'), this route will be '/cart/product/<product_id>'
## add option to add more product in the cart sections
@cart_bp.route('/cart/update', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0)) # Get the new quantity

    if product_id:
        cart = get_cart_from_session()

        if quantity > 0:
            # Update the quantity if it's greater than 0
            cart[product_id] = quantity
        elif product_id in cart:
            # Remove the item if quantity is 0 or less
            del cart[product_id]

        session['cart'] = cart
        # Clear previously calculated shipping cost as cart has changed
        session.pop('shipping_calculated_for_cart', None)
        session.pop('cart_shipping_quote_raw_usd', None)

    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/calculate_shipping', methods=['POST'])
def calculate_cart_shipping():
    cart_items_raw = get_cart_from_session()

    if not cart_items_raw:
        session.pop('shipping_calculated_for_cart', None)
        session.pop('cart_shipping_quote_raw_usd', None)
        return redirect(url_for('cart.view_cart'))

    # Use a mock address for cart page shipping calculation.
    # get_shipping_quote uses len(items) for its calculation.
    mock_address = "Cart Shipping Estimate"
    shipping_cost_usd, _ = get_shipping_quote(mock_address, cart_items_raw) # Assumes quote is in USD

    session['cart_shipping_quote_raw_usd'] = shipping_cost_usd
    session['shipping_calculated_for_cart'] = True
    
    return redirect(url_for('cart.view_cart'))
    

@cart_bp.route('/product/<product_id>') # Corrected to use cart_bp
def product_detail(product_id):
    target_currency = session.get('user_currency', 'USD') # Get target currency from session or default

    # Use the new function from product_service to get product details with converted price
    product_display_info = get_product_for_display(product_id, target_currency)

    if not product_display_info:
        return "Product not found", 404

    return render_template('product_detail.html', 
                           product=product_display_info,  # Pass the enriched product dictionary
                           displayed_price=product_display_info['displayed_price'], 
                           currency=product_display_info['displayed_currency'])

def empty_cart():
    """
    Function to be called by the checkout service after an order is placed.
    This removes the 'cart' key from the session dictionary.
    """
    session.pop('cart', None)
