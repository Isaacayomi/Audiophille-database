from fastapi import FastAPI, HTTPException
from database import get_connection

app = FastAPI()


@app.get("/products/category/{category}")
def get_category_products(category: str):
    conn = get_connection()
    cur = conn.cursor()

    # Fetch products basic info
    cur.execute("""
        SELECT id, slug, name, short_name, category, category_label, is_new, price, description, category_order
        FROM products
        WHERE category = %s
        ORDER BY category_order ASC
    """, (category,))
    rows = cur.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="No products found")

    products = []

    for row in rows:
        product_id = row[0]

        # Fetch category images
        cur.execute("""
            SELECT device, url FROM product_images
            WHERE product_id = %s AND context='category'
        """, (product_id,))
        category_images = {device: url for device, url in cur.fetchall()}

        # Fetch product images
        cur.execute("""
            SELECT device, url FROM product_images
            WHERE product_id = %s AND context='product'
        """, (product_id,))
        product_images = {device: url for device, url in cur.fetchall()}

        # Fetch gallery images
        gallery = {}
        for i in range(1, 4):
            cur.execute("""
                SELECT device, url FROM product_images
                WHERE product_id = %s AND context = %s
            """, (product_id, f'gallery_{i}'))
            gallery[f"{['first', 'second', 'third'][i - 1]}"] = {device: url for device, url in cur.fetchall()}

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