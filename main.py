import os
from typing import List, Optional

import stripe
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

from database import get_connection

app = FastAPI()

# Normalize allowed frontend origins so local and deployed clients can both call this API.
allowed_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,https://prime-audiophille-ecommerce.vercel.app",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stripe is configured once from environment variables at app startup.
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")


class CheckoutCustomer(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    zipCode: str
    city: str
    country: str


class CheckoutCartItem(BaseModel):
    slug: str
    name: str
    shortName: str
    price: int
    image: str
    quantity: int


class CheckoutPayload(BaseModel):
    customer: CheckoutCustomer
    cartItems: List[CheckoutCartItem]


# Product image groups mirror the storefront's mobile/tablet/desktop structure.
class ProductImageSet(BaseModel):
    mobile: str = ""
    tablet: str = ""
    desktop: str = ""


# Included items shown on the product detail page.
class ProductInclude(BaseModel):
    quantity: int
    item: str


# Related product cards shown in the "You May Also Like" section.
class ProductOther(BaseModel):
    slug: str
    category: str
    name: str
    image: ProductImageSet


# Gallery images shown on the product detail page.
class ProductGallery(BaseModel):
    first: ProductImageSet = Field(default_factory=ProductImageSet)
    second: ProductImageSet = Field(default_factory=ProductImageSet)
    third: ProductImageSet = Field(default_factory=ProductImageSet)


# Full product payload used by the admin dashboard for create/update requests.
class ProductPayload(BaseModel):
    slug: str
    category: str
    categoryLabel: str
    shortName: str
    name: str
    isNew: bool = False
    price: int
    description: str
    categoryOrder: int = 0
    features: List[str] = Field(default_factory=list)
    includes: List[ProductInclude] = Field(default_factory=list)
    categoryImage: ProductImageSet = Field(default_factory=ProductImageSet)
    productImage: ProductImageSet = Field(default_factory=ProductImageSet)
    gallery: ProductGallery = Field(default_factory=ProductGallery)
    others: List[ProductOther] = Field(default_factory=list)
    stock: int = 0
    status: str = "Draft"
    featured: bool = False
    image: str = ""
    storefrontPath: str = ""


def empty_image_set() -> dict:
    return {"mobile": "", "tablet": "", "desktop": ""}


def build_product_payload(cur, row):
    product_id = row[0]

    cur.execute("SELECT feature FROM features WHERE product_id = %s", (product_id,))
    features = [f[0] for f in cur.fetchall()]

    cur.execute("SELECT item, quantity FROM includes WHERE product_id = %s", (product_id,))
    includes = [{"item": i[0], "quantity": i[1]} for i in cur.fetchall()]

    cur.execute("""
        SELECT device, context, url
        FROM product_images
        WHERE product_id = %s
    """, (product_id,))
    images = cur.fetchall()

    category_image = {}
    product_image = {}
    gallery = {"first": {}, "second": {}, "third": {}}

    for device, context, url in images:
        if context == "category":
            category_image[device] = url
        elif context == "product":
            product_image[device] = url
        elif context.startswith("gallery_"):
            index = int(context.split("_")[1]) - 1
            key = ["first", "second", "third"][index]
            gallery[key][device] = url

    cur.execute("""
        SELECT p.id, p.slug, p.category, p.name
        FROM related_products rp
        JOIN products p ON p.id = rp.related_product_id
        WHERE rp.product_id = %s
    """, (product_id,))
    related_rows = cur.fetchall()

    others = []

    for related_id, related_slug, related_category, related_name in related_rows:
        cur.execute("""
            SELECT device, url
            FROM product_images
            WHERE product_id = %s AND context = 'category'
        """, (related_id,))
        related_image = {device: url for device, url in cur.fetchall()}

        others.append({
            "slug": related_slug,
            "category": related_category,
            "name": related_name,
            "image": related_image,
        })

    return {
        "id": product_id,
        "slug": row[1],
        "name": row[2],
        "shortName": row[3],
        "category": row[4],
        "categoryLabel": row[5],
        "isNew": row[6],
        "price": row[7],
        "description": row[8],
        "categoryOrder": row[9],
        "features": features,
        "includes": includes,
        "categoryImage": category_image,
        "productImage": product_image,
        "gallery": gallery,
        "others": others,
    }


def build_admin_product_payload(cur, row):
    # Reuse the storefront payload and add admin-only catalog fields.
    product = build_product_payload(cur, row)
    product.update({
        "stock": row[10],
        "status": row[11],
        "featured": row[12],
        "image": row[13],
        "storefrontPath": row[14],
    })
    return product


def resolve_image_set(value: ProductImageSet, fallback_url: str) -> ProductImageSet:
    # If the caller does not send image sizes, we reuse the main image as a safe fallback.
    if value.mobile or value.tablet or value.desktop:
        return value

    return ProductImageSet(mobile=fallback_url, tablet=fallback_url, desktop=fallback_url)


def upsert_product_related_data(cur, product_id: int, payload: ProductPayload) -> None:
    # Replace the product's feature, include, image, and related-product records.
    cur.execute("DELETE FROM features WHERE product_id = %s", (product_id,))
    cur.execute("DELETE FROM includes WHERE product_id = %s", (product_id,))
    cur.execute("DELETE FROM product_images WHERE product_id = %s", (product_id,))
    cur.execute("DELETE FROM related_products WHERE product_id = %s", (product_id,))

    for feature in payload.features or [payload.description]:
        cur.execute(
            "INSERT INTO features (product_id, feature) VALUES (%s, %s)",
            (product_id, feature),
        )

    includes = payload.includes or [ProductInclude(quantity=1, item="Product unit")]
    for item in includes:
        cur.execute(
            "INSERT INTO includes (product_id, item, quantity) VALUES (%s, %s, %s)",
            (product_id, item.item, item.quantity),
        )

    def insert_image(context: str, value: ProductImageSet) -> None:
        for device, url in value.model_dump().items():
            if url:
                cur.execute(
                    "INSERT INTO product_images (product_id, device, context, url) VALUES (%s, %s, %s, %s)",
                    (product_id, device, context, url),
                )

    fallback_images = ProductImageSet(mobile=payload.image, tablet=payload.image, desktop=payload.image)
    insert_image("category", resolve_image_set(payload.categoryImage, payload.image))
    insert_image("product", resolve_image_set(payload.productImage, payload.image))
    insert_image("gallery_1", resolve_image_set(payload.gallery.first, payload.image))
    insert_image("gallery_2", resolve_image_set(payload.gallery.second, payload.image))
    insert_image("gallery_3", resolve_image_set(payload.gallery.third, payload.image))

    for other in payload.others or []:
        cur.execute("SELECT id FROM products WHERE slug = %s", (other.slug,))
        other_row = cur.fetchone()
        if other_row:
            cur.execute(
                "INSERT INTO related_products (product_id, related_product_id) VALUES (%s, %s)",
                (product_id, other_row[0]),
            )


def persist_product(cur, payload: ProductPayload, existing_id: Optional[int] = None) -> int:
    # Insert or update the base product row, then synchronize its child tables.
    storefront_path = payload.storefrontPath or f"/{payload.category}/{payload.slug}"

    if existing_id is None:
        cur.execute(
            """
            INSERT INTO products (
                slug, name, short_name, category, category_label, is_new,
                price, description, category_order, stock, status, featured, image, storefront_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """,
            (
                payload.slug,
                payload.name,
                payload.shortName,
                payload.category,
                payload.categoryLabel,
                payload.isNew,
                payload.price,
                payload.description,
                payload.categoryOrder,
                payload.stock,
                payload.status,
                payload.featured,
                payload.image,
                storefront_path,
            ),
        )
        product_id = cur.fetchone()[0]
    else:
        cur.execute(
            """
            UPDATE products
            SET slug = %s,
                name = %s,
                short_name = %s,
                category = %s,
                category_label = %s,
                is_new = %s,
                price = %s,
                description = %s,
                category_order = %s,
                stock = %s,
                status = %s,
                featured = %s,
                image = %s,
                storefront_path = %s
            WHERE id = %s
        """,
            (
                payload.slug,
                payload.name,
                payload.shortName,
                payload.category,
                payload.categoryLabel,
                payload.isNew,
                payload.price,
                payload.description,
                payload.categoryOrder,
                payload.stock,
                payload.status,
                payload.featured,
                payload.image,
                storefront_path,
                existing_id,
            ),
        )
        product_id = existing_id

    upsert_product_related_data(cur, product_id, payload)
    return product_id


def fetch_products(cur, category: Optional[str] = None):
    # Load the full admin-facing product record list, optionally filtered by category.
    if category:
        cur.execute(
            """
            SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order, stock, status, featured, image, storefront_path
            FROM products
            WHERE LOWER(category) = %s
            ORDER BY category_order ASC
        """,
            (category.lower(),),
        )
    else:
        cur.execute(
            """
            SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order, stock, status, featured, image, storefront_path
            FROM products
            ORDER BY category, category_order ASC
        """
        )

    rows = cur.fetchall()
    return [build_admin_product_payload(cur, row) for row in rows]


# Admin/product API: list every product for the dashboard and sync flow.
@app.get("/products")
def get_products():
    conn = get_connection()
    cur = conn.cursor()

    try:
        products = fetch_products(cur)
        return {"products": products}
    finally:
        cur.close()
        conn.close()


# Storefront/admin API: list every product in one category, in catalog order.
@app.get("/products/category/{category}")
def get_category_products(category: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        products = fetch_products(cur, category)

        if not products:
            raise HTTPException(status_code=404, detail="No products found")

        return products
    finally:
        cur.close()
        conn.close()


# Admin/product API: get a single product by slug so the edit form can preload it.
@app.get("/products/{slug}")
def get_product_by_slug(slug: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order, stock, status, featured, image, storefront_path
        FROM products
        WHERE slug = %s
    """, (slug,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    product = build_admin_product_payload(cur, row)

    cur.close()
    conn.close()

    return {"product": product}


# Admin/product API: create a new product and its related tables.
@app.post("/products")
def create_product(payload: ProductPayload):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM products WHERE slug = %s", (payload.slug,))
        if cur.fetchone():
            raise HTTPException(status_code=409, detail="Product already exists")

        product_id = persist_product(cur, payload)
        conn.commit()
        cur.execute(
            """
            SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order, stock, status, featured, image, storefront_path
            FROM products
            WHERE id = %s
        """,
            (product_id,),
        )
        row = cur.fetchone()
        return {"product": build_admin_product_payload(cur, row)}
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


# Admin/product API: update an existing product by slug.
@app.put("/products/{slug}")
def update_product(slug: str, payload: ProductPayload):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM products WHERE slug = %s", (slug,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Product not found")

        product_id = persist_product(cur, payload, existing_id=row[0])
        conn.commit()
        cur.execute(
            """
            SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order, stock, status, featured, image, storefront_path
            FROM products
            WHERE id = %s
        """,
            (product_id,),
        )
        updated_row = cur.fetchone()
        return {"product": build_admin_product_payload(cur, updated_row)}
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


# Admin/product API: delete a product and all of its related child rows.
@app.delete("/products/{slug}")
def delete_product(slug: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM products WHERE slug = %s", (slug,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Product not found")

        product_id = row[0]

        cur.execute(
            "DELETE FROM related_products WHERE product_id = %s OR related_product_id = %s",
            (product_id, product_id),
        )
        cur.execute("DELETE FROM features WHERE product_id = %s", (product_id,))
        cur.execute("DELETE FROM includes WHERE product_id = %s", (product_id,))
        cur.execute("DELETE FROM product_images WHERE product_id = %s", (product_id,))
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()

        return {"deleted": True}
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


@app.get("/product/{slug}")
def get_product_by_slug(slug: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order
        FROM products
        WHERE slug = %s
    """, (slug,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    product = build_product_payload(cur, row)

    cur.close()
    conn.close()

    return {"product": product}


@app.get("/product/{category}/{slug}")
def get_product(category: str, slug: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order
        FROM products
        WHERE LOWER(category) = %s AND slug = %s
    """, (category.lower(), slug))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    product = build_product_payload(cur, row)

    cur.close()
    conn.close()

    return {"product": product}


def resolve_checkout_origin(request: Request) -> str:
    # Prefer the calling frontend origin, but only if it matches the configured allowlist.
    origin = request.headers.get("origin", "").strip().rstrip("/")

    if origin and origin in allowed_origins:
        return origin

    return FRONTEND_URL


@app.post("/payments/create-checkout-session")
def create_checkout_session(payload: CheckoutPayload, request: Request):
    # Stripe cannot create a Checkout Session if the secret key is missing.
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Missing STRIPE_SECRET_KEY")

    if not payload.cartItems:
        raise HTTPException(status_code=400, detail="Cart is empty")

    try:
        origin = resolve_checkout_origin(request)

        # Stripe expects amounts in cents, so product prices are multiplied by 100.
        line_items = []
        for item in payload.cartItems:
            line_items.append({
                "quantity": item.quantity,
                "price_data": {
                    "currency": "usd",
                    "unit_amount": item.price * 100,
                    "product_data": {
                        "name": item.name,
                        "metadata": {
                            "slug": item.slug,
                            "short_name": item.shortName,
                        },
                    },
                },
            })

        # The hosted Checkout page handles the secure payment step and redirects back afterward.
        session = stripe.checkout.Session.create(
            mode="payment",
            customer_email=payload.customer.email,
            billing_address_collection="required",
            phone_number_collection={"enabled": True},
            shipping_options=[
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {
                            "amount": 5000,
                            "currency": "usd",
                        },
                        "display_name": "Standard shipping",
                    }
                }
            ],
            line_items=line_items,
            success_url=f"{origin}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{origin}/checkout",
            metadata={
                "customerName": payload.customer.name,
                "customerPhone": payload.customer.phone,
                "shippingAddress": payload.customer.address,
                "shippingCity": payload.customer.city,
                "shippingZipCode": payload.customer.zipCode,
                "shippingCountry": payload.customer.country,
            },
        )

        if not session.url:
            raise HTTPException(status_code=500, detail="Stripe did not return a checkout URL")

        return {"url": session.url}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/payments/webhook")
async def stripe_webhook(request: Request):
    # Webhook verification ensures the event was actually sent by Stripe.
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Missing STRIPE_WEBHOOK_SECRET")

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Save the paid order to your database here when you're ready.
        # Example:
        # conn = get_connection()
        # cur = conn.cursor()
        # cur.execute(...)
        # conn.commit()
        # cur.close()
        # conn.close()

        print("Payment completed:", session["id"])

    return {"received": True}
