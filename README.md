# Audiophille API

## Overview
This project provides the core backend services for an e-commerce platform specializing in audio equipment. It manages the full product catalog and securely handles customer checkout processes. Essentially, it gives an online storefront a solid, reliable foundation for managing inventory and taking payments, making it easier to run an audio gear shop.

## Features
-   **Comprehensive Product Catalog**: Easily manage a detailed product catalog, including features, included items, and multi-device images.
-   **Category-Based Product Listings**: Retrieve products filtered by category, ordered for display on a storefront.
-   **Product Administration (CRUD)**: Create, retrieve, update, and delete product listings through dedicated admin endpoints.
-   **Secure Checkout Integration**: Process customer orders securely using Stripe Checkout Sessions, supporting various payment methods and shipping options.
-   **Stripe Webhook Handling**: Automatically receive and process payment confirmations and other events from Stripe.
-   **Flexible CORS Configuration**: Supports multiple frontend origins for seamless integration with both local and deployed storefronts.

## Getting Started
To get this API up and running on your local machine, follow these steps.

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Isaacayomi/Audiophille-database.git
    cd Audiophille-database
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    ```

3.  **Activate the Virtual Environment**:
    -   **On macOS and Linux**:
        ```bash
        source .venv/bin/activate
        ```
    -   **On Windows (Command Prompt)**:
        ```bash
        .venv\Scripts\activate.bat
        ```
    -   **On Windows (PowerShell)**:
        ```bash
        .venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables
You'll need to set up a `.env` file in the root of your project to configure database connections, Stripe API keys, and allowed frontend origins. Here's what you'll need:

| Variable                | Description                                                          | Example Value                                                 |
| :---------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------ |
| `DB_URL`                | Connection string for your PostgreSQL database.                      | `postgresql://user:password@host:port/database`               |
| `ALLOWED_ORIGINS`       | Comma-separated list of allowed frontend URLs for CORS.              | `http://localhost:3000,https://your-frontend.vercel.app`      |
| `FRONTEND_URL`          | The default frontend URL for redirects after Stripe Checkout.        | `http://localhost:3000`                                       |
| `STRIPE_SECRET_KEY`     | Your Stripe secret API key (starts with `sk_`).                     | `sk_test_YOUR_STRIPE_SECRET_KEY`                              |
| `STRIPE_WEBHOOK_SECRET` | Your Stripe webhook secret for verifying incoming webhook events.    | `whsec_YOUR_STRIPE_WEBHOOK_SECRET`                            |

Example `.env` file:
```dotenv
DB_URL="postgresql://user:password@localhost:5432/audiophille_db"
ALLOWED_ORIGINS="http://localhost:3000,https://prime-audiophille-ecommerce.vercel.app"
FRONTEND_URL="http://localhost:3000"
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
```

## Usage

1.  **Prepare the Database**:
    First, make sure your PostgreSQL database is running. Then, run the `seed.py` script to create the necessary tables and populate them with initial product data.
    ```bash
    python seed.py
    ```

2.  **Start the API Server**:
    With your virtual environment active and `.env` configured, you can start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be accessible at `http://localhost:8000`.

3.  **Interact with the API**:
    You can now make requests to the API endpoints. For example, to get all products:
    ```bash
    curl http://localhost:8000/products
    ```

## API Documentation

### Base URL
`http://localhost:8000`

### Endpoints

#### GET `/products`
Retrieves a list of all products, including admin-specific fields like `stock` and `status`.

**Response**:
```json
{
  "products": [
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
        "first": { "mobile": "...", "tablet": "...", "desktop": "..." },
        "second": { "mobile": "...", "tablet": "...", "desktop": "..." },
        "third": { "mobile": "...", "tablet": "...", "desktop": "..." }
      },
      "others": [
        {
          "slug": "xx99-mark-one-headphones",
          "category": "headphones",
          "name": "XX99 Mark I",
          "image": { "mobile": "...", "tablet": "...", "desktop": "..." }
        }
      ],
      "stock": 100,
      "status": "Published",
      "featured": true,
      "image": "/assets/product-xx99-mark-two-headphones/mobile/image-product.jpg",
      "storefrontPath": "/headphones/xx99-mark-two-headphones"
    }
  ]
}
```

#### GET `/products/category/{category}`
Fetches a list of products belonging to a specific category, ordered by `categoryOrder`.

**Path Parameters**:
-   `category`: The product category (e.g., `headphones`, `speakers`, `earphones`).

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
    "features": [],
    "includes": [],
    "categoryImage": {},
    "productImage": {},
    "gallery": { "first": {}, "second": {}, "third": {} },
    "others": [],
    "stock": 100,
    "status": "Published",
    "featured": true,
    "image": "/assets/product-xx99-mark-two-headphones/mobile/image-product.jpg",
    "storefrontPath": "/headphones/xx99-mark-two-headphones"
  }
]
```

**Errors**:
-   404: No products found for the given category.

#### GET `/products/{slug}`
Retrieves a single product by its slug, including all admin-facing details. This is typically used for admin dashboards.

**Path Parameters**:
-   `slug`: The unique identifier for the product (e.g., `xx99-mark-two-headphones`).

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
      "first": { "mobile": "...", "tablet": "...", "desktop": "..." },
      "second": { "mobile": "...", "tablet": "...", "desktop": "..." },
      "third": { "mobile": "...", "tablet": "...", "desktop": "..." }
    },
    "others": [
      {
        "slug": "xx99-mark-one-headphones",
        "category": "headphones",
        "name": "XX99 Mark I",
        "image": { "mobile": "...", "tablet": "...", "desktop": "..." }
      }
    ],
    "stock": 100,
    "status": "Published",
    "featured": true,
    "image": "/assets/product-xx99-mark-two-headphones/mobile/image-product.jpg",
    "storefrontPath": "/headphones/xx99-mark-two-headphones"
  }
}
```

**Errors**:
-   404: Product not found.

#### POST `/products`
Creates a new product entry in the database.

**Request**:
```json
{
  "slug": "new-product-slug",
  "category": "headphones",
  "categoryLabel": "Headphones",
  "shortName": "New Prod",
  "name": "New Product Name",
  "isNew": true,
  "price": 500,
  "description": "A description for the new product.",
  "categoryOrder": 4,
  "features": [
    "Feature one",
    "Feature two"
  ],
  "includes": [
    { "quantity": 1, "item": "Product unit" }
  ],
  "categoryImage": {
    "mobile": "/assets/new-product/mobile/category.jpg",
    "tablet": "/assets/new-product/tablet/category.jpg",
    "desktop": "/assets/new-product/desktop/category.jpg"
  },
  "productImage": {
    "mobile": "/assets/new-product/mobile/product.jpg",
    "tablet": "/assets/new-product/tablet/product.jpg",
    "desktop": "/assets/new-product/desktop/product.jpg"
  },
  "gallery": {
    "first": { "mobile": "...", "tablet": "...", "desktop": "..." }
  },
  "others": [
    { "slug": "xx99-mark-two-headphones", "category": "headphones", "name": "XX99 Mark II", "image": { "mobile": "...", "tablet": "...", "desktop": "..." } }
  ],
  "stock": 50,
  "status": "Draft",
  "featured": false,
  "image": "/assets/new-product/mobile/product.jpg",
  "storefrontPath": "/headphones/new-product-slug"
}
```

**Response**:
```json
{
  "product": {
    "id": 7,
    "slug": "new-product-slug",
    "name": "New Product Name",
    "shortName": "New Prod",
    "category": "headphones",
    "categoryLabel": "Headphones",
    "isNew": true,
    "price": 500,
    "description": "A description for the new product.",
    "categoryOrder": 4,
    "features": [
      "Feature one",
      "Feature two"
    ],
    "includes": [
      { "item": "Product unit", "quantity": 1 }
    ],
    "categoryImage": {
      "mobile": "/assets/new-product/mobile/category.jpg",
      "tablet": "/assets/new-product/tablet/category.jpg",
      "desktop": "/assets/new-product/desktop/category.jpg"
    },
    "productImage": {
      "mobile": "/assets/new-product/mobile/product.jpg",
      "tablet": "/assets/new-product/tablet/product.jpg",
      "desktop": "/assets/new-product/desktop/product.jpg"
    },
    "gallery": {
      "first": { "mobile": "...", "tablet": "...", "desktop": "..." },
      "second": { "mobile": "", "tablet": "", "desktop": "" },
      "third": { "mobile": "", "tablet": "", "desktop": "" }
    },
    "others": [
      {
        "slug": "xx99-mark-two-headphones",
        "category": "headphones",
        "name": "XX99 Mark II",
        "image": { "mobile": "...", "tablet": "...", "desktop": "..." }
      }
    ],
    "stock": 50,
    "status": "Draft",
    "featured": false,
    "image": "/assets/new-product/mobile/product.jpg",
    "storefrontPath": "/headphones/new-product-slug"
  }
}
```

**Errors**:
-   409: Product with the given slug already exists.
-   500: Internal server error.

#### PUT `/products/{slug}`
Updates an existing product identified by its slug.

**Path Parameters**:
-   `slug`: The unique identifier for the product to update.

**Request**:
```json
{
  "slug": "existing-product-slug",
  "category": "headphones",
  "categoryLabel": "Headphones",
  "shortName": "Updated Prod",
  "name": "Updated Product Name",
  "isNew": false,
  "price": 600,
  "description": "An updated description for the product.",
  "categoryOrder": 4,
  "features": [
    "Updated feature one"
  ],
  "includes": [
    { "quantity": 2, "item": "Updated unit" }
  ],
  "categoryImage": {
    "mobile": "/assets/existing-product/mobile/category-updated.jpg",
    "tablet": "/assets/existing-product/tablet/category-updated.jpg",
    "desktop": "/assets/existing-product/desktop/category-updated.jpg"
  },
  "productImage": {
    "mobile": "/assets/existing-product/mobile/product-updated.jpg",
    "tablet": "/assets/existing-product/tablet/product-updated.jpg",
    "desktop": "/assets/existing-product/desktop/product-updated.jpg"
  },
  "gallery": {
    "first": { "mobile": "...", "tablet": "...", "desktop": "..." }
  },
  "others": [],
  "stock": 45,
  "status": "Published",
  "featured": true,
  "image": "/assets/existing-product/mobile/product-updated.jpg",
  "storefrontPath": "/headphones/existing-product-slug"
}
```

**Response**:
```json
{
  "product": {
    "id": 7,
    "slug": "existing-product-slug",
    "name": "Updated Product Name",
    "shortName": "Updated Prod",
    "category": "headphones",
    "categoryLabel": "Headphones",
    "isNew": false,
    "price": 600,
    "description": "An updated description for the product.",
    "categoryOrder": 4,
    "features": [
      "Updated feature one"
    ],
    "includes": [
      { "item": "Updated unit", "quantity": 2 }
    ],
    "categoryImage": {
      "mobile": "/assets/existing-product/mobile/category-updated.jpg",
      "tablet": "/assets/existing-product/tablet/category-updated.jpg",
      "desktop": "/assets/existing-product/desktop/category-updated.jpg"
    },
    "productImage": {
      "mobile": "/assets/existing-product/mobile/product-updated.jpg",
      "tablet": "/assets/existing-product/tablet/product-updated.jpg",
      "desktop": "/assets/existing-product/desktop/product-updated.jpg"
    },
    "gallery": {
      "first": { "mobile": "...", "tablet": "...", "desktop": "..." },
      "second": { "mobile": "", "tablet": "", "desktop": "" },
      "third": { "mobile": "", "tablet": "", "desktop": "" }
    },
    "others": [],
    "stock": 45,
    "status": "Published",
    "featured": true,
    "image": "/assets/existing-product/mobile/product-updated.jpg",
    "storefrontPath": "/headphones/existing-product-slug"
  }
}
```

**Errors**:
-   404: Product not found.
-   500: Internal server error.

#### DELETE `/products/{slug}`
Deletes a product and all its associated data (features, includes, images, related products).

**Path Parameters**:
-   `slug`: The unique identifier for the product to delete.

**Response**:
```json
{
  "deleted": true
}
```

**Errors**:
-   404: Product not found.
-   500: Internal server error.

#### GET `/product/{slug}`
Retrieves a single product by its slug, optimized for storefront display (without admin-specific fields like stock, status, featured, etc.).

**Path Parameters**:
-   `slug`: The unique identifier for the product (e.g., `xx99-mark-two-headphones`).

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
      "first": { "mobile": "...", "tablet": "...", "desktop": "..." },
      "second": { "mobile": "...", "tablet": "...", "desktop": "..." },
      "third": { "mobile": "...", "tablet": "...", "desktop": "..." }
    },
    "others": [
      {
        "slug": "xx99-mark-one-headphones",
        "category": "headphones",
        "name": "XX99 Mark I",
        "image": { "mobile": "...", "tablet": "...", "desktop": "..." }
      }
    ]
  }
}
```

**Errors**:
-   404: Product not found.

#### GET `/product/{category}/{slug}`
Retrieves a single product by its category and slug, optimized for storefront display. This helps ensure the product is in the correct category context.

**Path Parameters**:
-   `category`: The product category (e.g., `headphones`).
-   `slug`: The unique identifier for the product.

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
      "first": { "mobile": "...", "tablet": "...", "desktop": "..." },
      "second": { "mobile": "...", "tablet": "...", "desktop": "..." },
      "third": { "mobile": "...", "tablet": "...", "desktop": "..." }
    },
    "others": [
      {
        "slug": "xx99-mark-one-headphones",
        "category": "headphones",
        "name": "XX99 Mark I",
        "image": { "mobile": "...", "tablet": "...", "desktop": "..." }
      }
    ]
  }
}
```

**Errors**:
-   404: Product not found.

#### POST `/payments/create-checkout-session`
Creates a new Stripe Checkout Session for processing an order. This will return a URL to Stripe's hosted checkout page.

**Request**:
```json
{
  "customer": {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "phone": "+1234567890",
    "address": "123 Main St",
    "zipCode": "90210",
    "city": "Beverly Hills",
    "country": "US"
  },
  "cartItems": [
    {
      "slug": "xx99-mark-two-headphones",
      "name": "XX99 Mark II Headphones",
      "shortName": "XX99 MK II",
      "price": 2999,
      "image": "/path/to/image.jpg",
      "quantity": 1
    },
    {
      "slug": "zx9-speaker",
      "name": "ZX9 Speaker",
      "shortName": "ZX9",
      "price": 4500,
      "image": "/path/to/speaker-image.jpg",
      "quantity": 2
    }
  ]
}
```

**Response**:
```json
{
  "url": "https://checkout.stripe.com/c/pay/cs_test_..."
}
```

**Errors**:
-   400: Cart is empty.
-   500: Missing `STRIPE_SECRET_KEY` or Stripe did not return a checkout URL.

#### POST `/payments/webhook`
Handles incoming Stripe webhook events, such as `checkout.session.completed`. This endpoint processes payment confirmations.

**Request**:
(Stripe sends a raw JSON payload and a `stripe-signature` header)

**Response**:
```json
{
  "received": true
}
```

**Errors**:
-   400: Missing `stripe-signature` header, invalid payload, or invalid signature.
-   500: Missing `STRIPE_WEBHOOK_SECRET`.

## Technologies Used

| Technology    | Description                                                      | Link                                                           |
| :------------ | :--------------------------------------------------------------- | :------------------------------------------------------------- |
| Python        | The primary programming language used.                           | [Python](https://www.python.org/)                              |
| FastAPI       | A modern, fast (high-performance) web framework for building APIs. | [FastAPI](https://fastapi.tiangolo.com/)                       |
| Pydantic      | Data validation and settings management using Python type hints. | [Pydantic](https://docs.pydantic.dev/latest/)                  |
| PostgreSQL    | A powerful, open-source relational database system.              | [PostgreSQL](https://www.postgresql.org/)                      |
| Psycopg2      | A PostgreSQL adapter for Python.                                 | [Psycopg2](https://www.psycopg.org/docs/)                      |
| Stripe        | A leading platform for online payment processing.                | [Stripe](https://stripe.com/)                                  |
| python-dotenv | Loads environment variables from a `.env` file.                  | [python-dotenv](https://pypi.org/project/python-dotenv/)       |
| Uvicorn       | An ASGI server for running Python web applications.              | [Uvicorn](https://www.uvicorn.org/)                            |

## Author Info

-   LinkedIn: [Isaac Ayomide Okunlola](https://www.linkedin.com/in/isaac-ayomide-okunlola-3568b7275/)
-   X (formerly Twitter): [Prime-codes](https://x.com/_devPRIME)

## Badges
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.12.5-E92063.svg)](https://docs.pydantic.dev/latest/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791.svg)](https://www.postgresql.org/)
[![Stripe](https://img.shields.io/badge/Stripe-Integration-635BFF.svg)](https://stripe.com/)
[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)
