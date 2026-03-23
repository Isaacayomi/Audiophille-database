# Audiophile E-commerce API Backend

## Overview
This project provides a robust backend API crafted with FastAPI, powering a modern e-commerce platform dedicated to premium audio products. It efficiently manages product catalog data using PostgreSQL and integrates seamlessly with Stripe for secure and streamlined payment processing.

## Features
-   **Python FastAPI**: High-performance, asynchronous web framework for building APIs with minimal boilerplate.
-   **Pydantic**: Data validation and settings management, ensuring robust and clear API request/response schemas.
-   **PostgreSQL**: Reliable and scalable relational database for storing product details, features, and related information.
-   **Stripe Integration**: Securely handles payment checkout sessions and processes webhook events for order fulfillment.
-   **`python-dotenv`**: Manages environment variables for secure and flexible configuration.
-   **CORS Middleware**: Configures Cross-Origin Resource Sharing to allow secure requests from specified frontend applications.

## Getting Started

To get this API backend up and running locally, follow these steps:

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Isaacayomi/Audiophille-database.git
    cd Audiophille-database # Adjust if your cloned directory has a different name
    ```

2.  **Create a Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up PostgreSQL Database**:
    *   Ensure you have a PostgreSQL server running.
    *   Create a new database for this project (e.g., `audiophile_db`).

5.  **Seed the Database**:
    The `seed.py` script will create the necessary tables and populate them with initial product data.
    ```bash
    python seed.py
    ```

6.  **Run the FastAPI Application**:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be accessible at `http://localhost:8000`.

### Environment Variables
Create a `.env` file in the root directory of the project and populate it with the following variables:

```dotenv
DB_URL="postgresql://user:password@host:port/database_name"
# OR individual components if preferred:
# DB_HOST="localhost"
# DB_NAME="audiophile_db"
# DB_USER="your_db_user"
# DB_PASSWORD="your_db_password"
# DB_PORT="5432"

STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

FRONTEND_URL="http://localhost:3000"
ALLOWED_ORIGINS="http://localhost:3000,https://prime-audiophille-ecommerce.vercel.app"
```

**Explanation:**
*   `DB_URL` (or individual `DB_HOST`, `DB_NAME`, etc.): Your PostgreSQL database connection string.
*   `STRIPE_SECRET_KEY`: Your secret key from Stripe. Required for creating checkout sessions. Obtain this from your [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys).
*   `STRIPE_WEBHOOK_SECRET`: Your webhook signing secret from Stripe. Essential for verifying webhook events. Obtain this when setting up a [Stripe Webhook Endpoint](https://dashboard.stripe.com/test/webhooks).
*   `FRONTEND_URL`: The base URL of your frontend application. Used for Stripe success/cancel redirects. Defaults to `http://localhost:3000`.
*   `ALLOWED_ORIGINS`: A comma-separated list of origins (frontend URLs) that are permitted to access this API via CORS.

## Usage

Once the server is running, you can interact with the API using tools like `curl`, Postman, or by integrating it with your frontend application.

**Example: Fetching products by category**
To retrieve all products within the 'headphones' category:

```bash
curl -X GET "http://localhost:8000/products/category/headphones" \
     -H "accept: application/json"
```

**Example: Fetching a single product by slug**
To retrieve details for the 'xx99-mark-two-headphones' product:

```bash
curl -X GET "http://localhost:8000/product/xx99-mark-two-headphones" \
     -H "accept: application/json"
```

**Example: Creating a Stripe Checkout Session**
To initiate a payment checkout process, send a POST request to the `/payments/create-checkout-session` endpoint with customer and cart item details.

```bash
curl -X POST "http://localhost:8000/payments/create-checkout-session" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
           "customer": {
             "name": "Jane Doe",
             "email": "jane.doe@example.com",
             "phone": "+1234567890",
             "address": "123 Commerce St",
             "zipCode": "10001",
             "city": "New York",
             "country": "US"
           },
           "cartItems": [
             {
               "slug": "xx99-mark-two-headphones",
               "name": "XX99 Mark II Headphones",
               "shortName": "XX99 MK II",
               "price": 2999,
               "image": "/assets/product-xx99-mark-two-headphones/mobile/image-product.jpg",
               "quantity": 1
             }
           ]
         }'
```
This will return a Stripe checkout URL, which your frontend can then redirect the user to.

## Technologies Used

| Technology    | Description                                                 |
| :------------ | :---------------------------------------------------------- |
| **Python**    | The primary programming language for the backend.           |
| **FastAPI**   | Modern, fast (high-performance) web framework for building APIs. |
| **Pydantic**  | Data validation and settings management using Python type hints. |
| **PostgreSQL**| Robust open-source relational database.                     |
| **Psycopg2**  | PostgreSQL adapter for Python.                              |
| **Stripe**    | Payment processing platform for e-commerce transactions.    |
| **Uvicorn**   | ASGI server for running FastAPI applications.               |
| **python-dotenv** | Reads key-value pairs from a `.env` file.                 |

## API Documentation
### Base URL
The API is served at the root path, typically `http://localhost:8000/` in a local development environment.

### Endpoints

#### GET /products/category/{category}
Retrieves a list of products belonging to a specific category, ordered by `category_order`.

**Request**:
This endpoint does not require a request body. The category is provided as a path parameter.

**Response**:
```json
[
  {
    "id": 1,
    "slug": "xx99-mark-two-headphones",
    "name": "XX99 Mark II Headphones",
    "shortName": "XX99 MK II",
    "category": "headphones",
    "categoryLabel": "Headphones",
    "isNew": true,
    "price": 2999,
    "description": "The new XX99 Mark II headphones is the pinnacle of pristine audio...",
    "categoryOrder": 1,
    "categoryImage": {
      "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-category-page-preview.jpg",
      "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-category-page-preview.jpg",
      "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-category-page-preview.jpg"
    },
    "productImage": {
      "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-product.jpg",
      "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-product.jpg",
      "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-product.jpg"
    },
    "gallery": {
      "first": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-1.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-1.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-1.jpg"
      },
      "second": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-2.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-2.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-2.jpg"
      },
      "third": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-3.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-3.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-3.jpg"
      }
    }
  }
  // ... more products
]
```

**Errors**:
-   `404 Not Found`: No products found for the specified category.

#### GET /product/{slug}
Retrieves the detailed information for a single product using its unique slug.

**Request**:
This endpoint does not require a request body. The product slug is provided as a path parameter.

**Response**:
```json
{
  "product": {
    "id": 1,
    "slug": "xx99-mark-two-headphones",
    "name": "XX99 Mark II Headphones",
    "shortName": "XX99 MK II",
    "category": "headphones",
    "categoryLabel": "Headphones",
    "isNew": true,
    "price": 2999,
    "description": "The new XX99 Mark II headphones is the pinnacle of pristine audio...",
    "categoryOrder": 1,
    "features": [
      "Featuring a genuine leather head strap...",
      "The advanced driver unit architecture..."
    ],
    "includes": [
      { "item": "Headphone unit", "quantity": 1 },
      { "item": "Replacement earcups", "quantity": 2 }
    ],
    "categoryImage": {
      "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-category-page-preview.jpg",
      "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-category-page-preview.jpg",
      "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-category-page-preview.jpg"
    },
    "productImage": {
      "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-product.jpg",
      "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-product.jpg",
      "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-product.jpg"
    },
    "gallery": {
      "first": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-1.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-1.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-1.jpg"
      },
      "second": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-2.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-2.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-2.jpg"
      },
      "third": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-3.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-3.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-3.jpg"
      }
    },
    "others": [
      {
        "slug": "xx99-mark-one-headphones",
        "category": "headphones",
        "name": "XX99 Mark I",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx99-mark-one-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx99-mark-one-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx99-mark-one-headphones.jpg"
        }
      }
    ]
  }
}
```

**Errors**:
-   `404 Not Found`: Product not found for the specified slug.

#### GET /product/{category}/{slug}
Retrieves the detailed information for a single product, filtered by both category and slug.

**Request**:
This endpoint does not require a request body. The category and product slug are provided as path parameters.

**Response**:
```json
{
  "product": {
    "id": 1,
    "slug": "xx99-mark-two-headphones",
    "name": "XX99 Mark II Headphones",
    "shortName": "XX99 MK II",
    "category": "headphones",
    "categoryLabel": "Headphones",
    "isNew": true,
    "price": 2999,
    "description": "The new XX99 Mark II headphones is the pinnacle of pristine audio...",
    "categoryOrder": 1,
    "features": [
      "Featuring a genuine leather head strap...",
      "The advanced driver unit architecture..."
    ],
    "includes": [
      { "item": "Headphone unit", "quantity": 1 },
      { "item": "Replacement earcups", "quantity": 2 }
    ],
    "categoryImage": {
      "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-category-page-preview.jpg",
      "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-category-page-preview.jpg",
      "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-category-page-preview.jpg"
    },
    "productImage": {
      "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-product.jpg",
      "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-product.jpg",
      "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-product.jpg"
    },
    "gallery": {
      "first": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-1.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-1.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-1.jpg"
      },
      "second": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-2.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-2.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-2.jpg"
      },
      "third": {
        "mobile": "/assets/product-xx99-mark-two-headphones/mobile/image-gallery-3.jpg",
        "tablet": "/assets/product-xx99-mark-two-headphones/tablet/image-gallery-3.jpg",
        "desktop": "/assets/product-xx99-mark-two-headphones/desktop/image-gallery-3.jpg"
      }
    },
    "others": [
      {
        "slug": "xx99-mark-one-headphones",
        "category": "headphones",
        "name": "XX99 Mark I",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx99-mark-one-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx99-mark-one-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx99-mark-one-headphones.jpg"
        }
      }
    ]
  }
}
```

**Errors**:
-   `404 Not Found`: Product not found for the specified category and slug combination.

#### POST /payments/create-checkout-session
Initiates a Stripe Checkout Session for payment processing. Requires customer details and a list of items in the cart.

**Request**:
```json
{
  "customer": {
    "name": "string",
    "email": "user@example.com",
    "phone": "string",
    "address": "string",
    "zipCode": "string",
    "city": "string",
    "country": "string"
  },
  "cartItems": [
    {
      "slug": "string",
      "name": "string",
      "shortName": "string",
      "price": 0,
      "image": "string",
      "quantity": 0
    }
  ]
}
```
**Required fields**:
-   `customer.name`: Customer's full name.
-   `customer.email`: Customer's email address (must be a valid email format).
-   `customer.phone`: Customer's phone number.
-   `customer.address`: Customer's street address.
-   `customer.zipCode`: Customer's postal/zip code.
-   `customer.city`: Customer's city.
-   `customer.country`: Customer's country.
-   `cartItems`: A list of product objects in the cart. Each item requires:
    -   `slug`: Product's unique slug.
    -   `name`: Product's full name.
    -   `shortName`: Product's short name.
    -   `price`: Product's price in base currency units (e.g., dollars, not cents).
    -   `image`: URL to the product image.
    -   `quantity`: Number of this product in the cart.

**Response**:
```json
{
  "url": "https://checkout.stripe.com/c/pay/..."
}
```

**Errors**:
-   `400 Bad Request`: `detail`: "Cart is empty".
-   `500 Internal Server Error`: `detail`: "Missing STRIPE_SECRET_KEY" or "Stripe did not return a checkout URL" or other Stripe-related processing errors.

#### POST /payments/webhook
Endpoint for Stripe webhook events. This API receives and processes events from Stripe, such as `checkout.session.completed`, for post-payment actions.

**Request**:
The request body is a raw JSON payload sent by Stripe. Additionally, a `stripe-signature` header is required for verification.

**Response**:
```json
{
  "received": true
}
```

**Errors**:
-   `400 Bad Request`:
    -   `detail`: "Missing stripe-signature header"
    -   `detail`: "Invalid payload" (if the raw body cannot be parsed by Stripe)
    -   `detail`: "Invalid signature" (if the `stripe-signature` does not match the payload and webhook secret)
-   `500 Internal Server Error`: `detail`: "Missing STRIPE_WEBHOOK_SECRET".

## Author Info

Connect with me and explore more of my work:

**[Your Name]**
*   **LinkedIn**: [Isaac Ayomide Okunlola](https://www.linkedin.com/in/isaac-ayomide-okunlola-3568b7275)
*   **X (formerly Twitter)**: [@_devPRIME](https://x.com/_devPRIME)

---
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.12.0-E92063.svg?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/latest/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791.svg?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Stripe](https://img.shields.io/badge/Stripe-Integration-626CD9.svg?style=flat-square&logo=stripe&logoColor=white)](https://stripe.com/)

[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)
