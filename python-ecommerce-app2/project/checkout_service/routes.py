from flask import render_template, request, redirect, url_for, flash
import uuid
from . import checkout_bp

# Import all the simulated services it depends on
from project.services import charge_card, get_shipping_quote, send_confirmation_email, convert_currency
# --- CORRECTED IMPORT ---
# Import the new session-based cart functions
from project.cart_service.routes import get_cart_from_session, empty_cart
from project.product_service.routes import get_product

@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # --- CORRECTED FUNCTION CALL ---
    # Get cart data from the session using the new function
    cart_items_raw = get_cart_from_session()

    if not cart_items_raw:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('frontend.home'))
        
    if request.method == 'POST':
        # 1. Validate cart items and calculate total price
        valid_items_for_order = []
        calculated_subtotal = 0
        all_items_valid = True

        for pid, qty in cart_items_raw.items():
            product = get_product(pid)
            if product and isinstance(product.get('price'), (int, float)):
                valid_items_for_order.append({'id': pid, 'qty': qty})
                calculated_subtotal += product['price'] * qty
            else:
                all_items_valid = False
                flash(f"Product with ID '{pid}' is invalid or out of stock and cannot be processed. Please review your cart.", "danger")


        if all_items_valid:
            # 2. Get shipping quote (call shipping service)
            shipping_cost, ship_id = get_shipping_quote(request.form['address'], valid_items_for_order)
            
            # 3. Calculate final total
            final_total = calculated_subtotal + shipping_cost

            # 4. Charge card (call payment service)
            charge_ok, trans_id = charge_card(request.form, final_total, 'USD')

            if not charge_ok:
                flash("Payment failed. Please try again.", "danger")
                # Fall through to render the checkout page again with the error
            else:
                # 5. Create order and send confirmation (call email service)
                order_id = str(uuid.uuid4())
                order_details = {'id': order_id, 'total': final_total, 'shipping_id': ship_id, 'transaction_id': trans_id}
                send_confirmation_email(request.form['email'], order_details)
                
                # 6. Empty the cart (call the session-based empty_cart function)
                empty_cart()

                return redirect(url_for('checkout.order_success', order_id=order_id))
        # If not all_items_valid, or if charge_ok was false, fall through to render template

    # This part is for the GET request or when POST fails and needs to re-render.
    # Calculate cart_total robustly for display.
    display_cart_total = 0
    # Potentially, also prepare a list of items for display if the template needs it.
    # display_items_list = [] 
    if cart_items_raw:
        for pid, qty in cart_items_raw.items():
            product = get_product(pid)
            if product and isinstance(product.get('price'), (int, float)):
                display_cart_total += product['price'] * qty
                # if template needs item details:
                # display_items_list.append({'name': product.get('name', pid), 'qty': qty, 'price': product['price']})
            # Else: product is invalid or has no price, skip for total.
            # A flash message here could be redundant if POST already flashed.
    return render_template('checkout.html', cart_total=display_cart_total) #, items=display_items_list)

@checkout_bp.route('/order_success')
def order_success():
    order_id = request.args.get('order_id')
    return render_template('order_success.html', order_id=order_id)


    