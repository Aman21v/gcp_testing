import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def charge_card(card_details, amount, currency):
    """Simulates charging a credit card via the Payment service."""
    logger.info(f"Charging card {card_details['number'][:4]}... for {amount} {currency}")
    # In a real app, this would call a payment gateway like Stripe or Braintree
    return True, "transaction_id_12345"

def send_confirmation_email(email, order_details):
    """Simulates sending an order confirmation via the Email service."""
    logger.info(f"Sending confirmation email to {email} for order {order_details['id']}.")
    # In a real app, this would use a service like SendGrid or Amazon SES
    return True

def get_shipping_quote(address, items):
    """Simulates getting a shipping quote from the Shipping service."""
    # Quote is based on the number of items for simplicity
    quote = 5.00 * len(items)
    logger.info(f"Calculated shipping quote for {len(items)} items to {address}: ${quote:.2f}")
    return quote, "shipping_id_abcde"

## get discount based on the cost of the product



def convert_currency(amount, from_currency, to_currency):
    """Simulates currency conversion from the Currency service."""
    # Mock conversion rates
    rates = {"USD": 1.0, "EUR": 0.92, "INR": 85.0}
    if from_currency not in rates or to_currency not in rates:
        return amount # Return original amount if currency is unknown
    
    # Convert to USD first, then to the target currency
    amount_in_usd = amount / rates[from_currency]
    converted_amount = amount_in_usd * rates[to_currency]
    logger.info(f"Converted {amount} {from_currency} to {converted_amount:.2f} {to_currency}")
    return round(converted_amount, 2)
