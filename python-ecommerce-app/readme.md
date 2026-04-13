# Microservices E-Commerce Flask App

This is a sample e-commerce application built with Flask, demonstrating a microservices-like architecture. Each core functionality (frontend, products, cart, checkout, ads) is organized into its own "service" (Flask Blueprint).

## Features

*   **Product Catalog:** View recommended products on the home page.
*   **Product Details:** View individual product details (though this route is currently within the cart service, ideally it would be in the product service).
*   **Shopping Cart:**
    *   Add products to the cart.
    *   View cart contents.
    *   Update item quantities in the cart.
    *   Remove items from the cart.
*   **Currency Conversion:** Display prices in USD, EUR, or INR. The selection can be made on the cart page.
*   **Checkout Process:** A simulated checkout flow including:
    *   Shipping address and payment information collection.
    *   Simulated calls to external services for shipping quotes and payment processing.
    *   Simulated order confirmation email.
*   **Advertisements:** Display mock ads on the home page.
*   **Session Management:** Uses Flask sessions, potentially backed by Redis for persistence (as suggested by `FlaskRedis` in `extensions.py`).

## Technology Stack

*   **Backend:** Python 3.x, Flask
*   **Frontend:** HTML, CSS, Jinja2 (Flask's templating engine)
*   **Session/Caching:** Redis (via `Flask-Redis`)
*   **Development Server:** Flask's built-in development server

## Project Structure

The project is structured into "microservices" using Flask Blueprints:

*   `project/`
    *   `frontend_service/`: Handles user-facing pages like home.
    *   `product_service/`: Manages product data and recommendations.
    *   `cart_service/`: Manages the shopping cart functionality.
    *   `checkout_service/`: Handles the order processing and checkout.
    *   `ad_service/`: Provides mock advertisements.
    *   `services.py`: Contains mock functions simulating external services (payment, email, shipping, currency conversion).
    *   `templates/`: HTML templates for the application.
    *   `static/`: Static files like CSS.
    *   `__init__.py`: Application factory.
    *   `extensions.py`: Flask extension initializations (e.g., Redis).
*   `run.py`: Script to start the Flask development server.
*   `requirements.txt`: Python dependencies.

## Setup and Running the Application

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd e-commerce-flask-app
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ensure Redis is running:**
    This application is configured to use Redis. Make sure you have a Redis server instance running on its default port (6379) or configure the `REDIS_URL` in `project/__init__.py` if needed.

5.  **Run the application:**
    ```bash
    python run.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/` or `http://0.0.0.0:5000/`.

## Notes

*   The "services" (payment, email, shipping, currency conversion) are currently mocked within `project/services.py`. In a real-world scenario, these would be independent services or third-party integrations.
*   The secret key in `project/__init__.py` is set to `'dev'`. For production, this **must** be changed to a strong, random secret.