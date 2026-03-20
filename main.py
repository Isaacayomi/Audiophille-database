from fastapi import FastAPI, HTTPException
from database import get_connection

app = FastAPI()


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
