# Audiophile Product Catalog API

## Overview
A robust Python FastAPI application designed to serve product catalog data for an e-commerce platform. This API leverages PostgreSQL for efficient data storage and retrieval, providing comprehensive product information including features, bundled items, multi-device images, and related products, all structured for seamless front-end consumption.

## Features
- **FastAPI**: Provides a high-performance, asynchronous web framework for building APIs.
- **PostgreSQL**: Stores and manages structured product data, including hierarchical relationships and detailed attributes.
- **`python-dotenv`**: Securely manages environment-specific configurations for database connections.
- **Detailed Product Retrieval**: Fetches extensive product details, including features, `what's in the box` items, diverse image sets, and related products, all consolidated into a single response.
- **Category-Based Product Listing**: Enables filtering and retrieval of products based on their categories, ordered for presentation.

## Getting Started
### Installation
To get this project up and running on your local machine, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Isaacayomi/Audiophille-database.git
    cd Audiophille-database
    ```

2.  **Create a Virtual Environment**:
    It is highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install Dependencies**:
    Install the required Python packages using pip.
    ```bash
    pip install fastapi uvicorn psycopg2-binary python-dotenv
    ```

5.  **Set up PostgreSQL Database**:
    Ensure you have a PostgreSQL server running. Create a new database for this project (e.g., `audiophile_db`).

6.  **Configure Environment Variables**:
    Create a `.env` file in the root directory of the project and populate it with your PostgreSQL database credentials.
    ```ini
    DB_HOST=localhost
    DB_NAME=audiophile_db
    DB_USER=your_username
    DB_PASSWORD=your_password
    DB_PORT=5432
    ```
    Replace `your_username`, `your_password`, and `audiophile_db` with your actual PostgreSQL credentials and database name.

7.  **Seed the Database**:
    Run the `seed.py` script to create the necessary tables and populate them with initial product data.
    ```bash
    python seed.py
    ```
    You should see "Database seeded successfully!" upon completion.

### Environment Variables
To run this application, the following environment variables must be defined in your `.env` file:

-   `DB_HOST`: The hostname of your PostgreSQL database server.
    *   Example: `DB_HOST=localhost`
-   `DB_NAME`: The name of the database to connect to.
    *   Example: `DB_NAME=audiophile_db`
-   `DB_USER`: The username for connecting to the database.
    *   Example: `DB_USER=postgres`
-   `DB_PASSWORD`: The password for the database user.
    *   Example: `DB_PASSWORD=mysecretpassword`
-   `DB_PORT`: The port number on which the PostgreSQL server is listening.
    *   Example: `DB_PORT=5432`

## Usage
To start the FastAPI application, run the following command from your project root:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reloading of the server when code changes are detected, which is convenient for development.

The API will be available at `http://127.0.0.1:8000` (or `http://localhost:8000`). You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs` and ReDoc at `http://127.0.0.1:8000/redoc`.

## Technologies Used

| Technology         | Description                                                      |
| :----------------- | :--------------------------------------------------------------- |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | The primary programming language used for the backend.         |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | A modern, fast (high-performance) web framework for building APIs with Python 3.7+. |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) | An open-source relational database system used for data storage. |
| ![Psycopg2](https://img.shields.io/badge/Psycopg2-4B8BBE?style=for-the-badge&logo=python&logoColor=white) | PostgreSQL adapter for Python, enabling database interaction. |
| ![python-dotenv](https://img.shields.io/badge/python--dotenv-F7DF1E?style=for-the-badge&logo=python&logoColor=black) | Manages environment variables from a `.env` file for secure configuration. |
| ![Uvicorn](https://img.shields.io/badge/Uvicorn-FFC107?style=for-the-badge&logo=python&logoColor=black) | An ASGI server implementation for Python, used to run FastAPI applications. |

## API Documentation
### Base URL
`http://127.0.0.1:8000`

### Endpoints
#### GET /products/category/{category}
Retrieves a list of products belonging to a specific category.

**Request**:
Path Parameters:
-   `category` (string, required): The name of the product category (e.g., "headphones", "speakers", "earphones").

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
    "description": "The new XX99 Mark II headphones is the pinnacle of pristine audio. It redefines your premium headphone experience by reproducing the balanced depth and precision of studio-quality sound.",
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
]
```

**Errors**:
-   `404 Not Found`: No products found for the specified category.

#### GET /product/{slug}
Retrieves detailed information for a single product using its unique slug.

**Request**:
Path Parameters:
-   `slug` (string, required): The unique slug of the product (e.g., "xx99-mark-two-headphones").

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
    "description": "The new XX99 Mark II headphones is the pinnacle of pristine audio. It redefines your premium headphone experience by reproducing the balanced depth and precision of studio-quality sound.",
    "categoryOrder": 1,
    "features": [
      "Featuring a genuine leather head strap and premium earcups, these headphones deliver superior comfort for those who like to enjoy endless listening. It includes intuitive controls designed for any situation, whether you're taking a business call or just in your own personal space. The active noise cancellation lets you immerse yourself in your audio and keeps distractions to a minimum.",
      "The advanced driver unit architecture creates a perfectly balanced response across the entire frequency range. Their detail-rich sound makes them the perfect companion for discerning listeners who care deeply about fidelity and craftsmanship."
    ],
    "includes": [
      {
        "item": "Headphone unit",
        "quantity": 1
      },
      {
        "item": "Replacement earcups",
        "quantity": 2
      },
      {
        "item": "User manual",
        "quantity": 1
      },
      {
        "item": "3.5mm 5m audio cable",
        "quantity": 1
      },
      {
        "item": "Travel bag",
        "quantity": 1
      }
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
      },
      {
        "slug": "xx59-headphones",
        "category": "headphones",
        "name": "XX59",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx59-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx59-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx59-headphones.jpg"
        }
      },
      {
        "slug": "zx9-speaker",
        "category": "speakers",
        "name": "ZX9 Speaker",
        "image": {
          "mobile": "/assets/shared/mobile/image-zx9-speaker.jpg",
          "tablet": "/assets/shared/tablet/image-zx9-speaker.jpg",
          "desktop": "/assets/shared/desktop/image-zx9-speaker.jpg"
        }
      }
    ]
  }
}
```

**Errors**:
-   `404 Not Found`: Product with the specified slug does not exist.

#### GET /product/{category}/{slug}
Retrieves detailed information for a single product, ensuring it belongs to the specified category.

**Request**:
Path Parameters:
-   `category` (string, required): The name of the product category.
-   `slug` (string, required): The unique slug of the product.

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
    "description": "The new XX99 Mark II headphones is the pinnacle of pristine audio. It redefines your premium headphone experience by reproducing the balanced depth and precision of studio-quality sound.",
    "categoryOrder": 1,
    "features": [
      "Featuring a genuine leather head strap and premium earcups, these headphones deliver superior comfort for those who like to enjoy endless listening. It includes intuitive controls designed for any situation, whether you're taking a business call or just in your own personal space. The active noise cancellation lets you immerse yourself in your audio and keeps distractions to a minimum.",
      "The advanced driver unit architecture creates a perfectly balanced response across the entire frequency range. Their detail-rich sound makes them the perfect companion for discerning listeners who care deeply about fidelity and craftsmanship."
    ],
    "includes": [
      {
        "item": "Headphone unit",
        "quantity": 1
      },
      {
        "item": "Replacement earcups",
        "quantity": 2
      },
      {
        "item": "User manual",
        "quantity": 1
      },
      {
        "item": "3.5mm 5m audio cable",
        "quantity": 1
      },
      {
        "item": "Travel bag",
        "quantity": 1
      }
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
      },
      {
        "slug": "xx59-headphones",
        "category": "headphones",
        "name": "XX59",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx59-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx59-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx59-headphones.jpg"
        }
      },
      {
        "slug": "zx9-speaker",
        "category": "speakers",
        "name": "ZX9 Speaker",
        "image": {
          "mobile": "/assets/shared/mobile/image-zx9-speaker.jpg",
          "tablet": "/assets/shared/tablet/image-zx9-speaker.jpg",
          "desktop": "/assets/shared/desktop/image-zx9-speaker.jpg"
        }
      }
    ]
  }
}
```

**Errors**:
-   `404 Not Found`: Product with the specified category and slug does not exist.

## License
This project is not currently licensed.

## Author Info
**Your Name Here**
*   LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com/in/your_username/)
*   X (formerly Twitter): [Your X Profile](https://x.com/your_username)

---
Made with Python and FastAPI.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Psycopg2](https://img.shields.io/badge/Psycopg2-4B8BBE?style=for-the-badge&logo=python&logoColor=white)](https://www.psycopg.org/)
[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)