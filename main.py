import os
from typing import List

import stripe
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

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


@app.get("/products/category/{category}")
def get_category_products(category: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order
        FROM products
        WHERE LOWER(category) = %s
        ORDER BY category_order ASC
    """, (category.lower(),))
    rows = cur.fetchall()

    if not rows:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="No products found")

    products = []

    for row in rows:
        product_id = row[0]

        cur.execute("""
            SELECT device, url FROM product_images
            WHERE product_id = %s AND context = 'category'
        """, (product_id,))
        category_images = {device: url for device, url in cur.fetchall()}

        cur.execute("""
            SELECT device, url FROM product_images
            WHERE product_id = %s AND context = 'product'
        """, (product_id,))
        product_images = {device: url for device, url in cur.fetchall()}

        gallery = {"first": {}, "second": {}, "third": {}}
        for i, key in enumerate(["first", "second", "third"], start=1):
            cur.execute("""
                SELECT device, url FROM product_images
                WHERE product_id = %s AND context = %s
            """, (product_id, f"gallery_{i}"))
            gallery[key] = {device: url for device, url in cur.fetchall()}

        products.append({
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
            "categoryImage": category_images,
            "productImage": product_images,
            "gallery": gallery,
        })

    cur.close()
    conn.close()

    return products


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
