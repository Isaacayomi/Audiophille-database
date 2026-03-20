import psycopg2

# Connect to PostgresSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="okanmife@07",
    port=5432
)

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# 2. Drop existing tables if there's any to start fresh
cur.execute("DROP TABLE IF EXISTS related_products CASCADE")
cur.execute("DROP TABLE IF EXISTS product_images CASCADE")
cur.execute("DROP TABLE IF EXISTS includes CASCADE")
cur.execute("DROP TABLE IF EXISTS features CASCADE")
cur.execute("DROP TABLE IF EXISTS products CASCADE")

# Create 'products' table
cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    short_name VARCHAR(255),
    category VARCHAR(50),
    category_label VARCHAR(50),
    is_new BOOLEAN DEFAULT FALSE,
    price INTEGER,
    description TEXT,
    category_order INTEGER
)
""")

# Create 'features' table
cur.execute("""
CREATE TABLE IF NOT EXISTS features (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    feature TEXT
)
""")

# Create 'includes' table
cur.execute("""
CREATE TABLE IF NOT EXISTS includes (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    item VARCHAR(255),
    quantity INT
)
""")

# Create 'product_images' table
cur.execute("""
CREATE TABLE IF NOT EXISTS product_images (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    device VARCHAR(20),   -- mobile, tablet, desktop
    context VARCHAR(50),  -- product, category, gallery_1, gallery_2, gallery_3
    url TEXT
)
""")

# Create 'related_products' table
cur.execute("""
CREATE TABLE IF NOT EXISTS related_products (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    related_product_id INT REFERENCES products(id) ON DELETE CASCADE
)
""")

# Commit table creation
conn.commit()

# Insert products and related data
products = [
    {
        "slug": "xx99-mark-two-headphones",
        "category": "headphones",
        "categoryLabel": "Headphones",
        "shortName": "XX99 MK II",
        "name": "XX99 Mark II Headphones",
        "isNew": True,
        "price": 2999,
        "description": "The new XX99 Mark II headphones is the pinnacle of pristine audio...",
        "features": [
            "Featuring a genuine leather head strap...",
            "The advanced driver unit architecture..."
        ],
        "includes": [
            {"quantity": 1, "item": "Headphone unit"},
            {"quantity": 2, "item": "Replacement earcups"},
            {"quantity": 1, "item": "User manual"},
            {"quantity": 1, "item": "3.5mm 5m audio cable"},
            {"quantity": 1, "item": "Travel bag"}
        ],
        "categoryImage": {
            "mobile": "category_mobile.jpg",
            "tablet": "category_tablet.jpg",
            "desktop": "category_desktop.jpg"
        },
        "productImage": {
            "mobile": "product_mobile.jpg",
            "tablet": "product_tablet.jpg",
            "desktop": "product_desktop.jpg"
        },
        "gallery": {
            "first": {"mobile": "g1_mobile.jpg", "tablet": "g1_tablet.jpg", "desktop": "g1_desktop.jpg"},
            "second": {"mobile": "g2_mobile.jpg", "tablet": "g2_tablet.jpg", "desktop": "g2_desktop.jpg"},
            "third": {"mobile": "g3_mobile.jpg", "tablet": "g3_tablet.jpg", "desktop": "g3_desktop.jpg"}
        },
        "others": [
            {"slug": "xx99-mark-one-headphones"},
            {"slug": "xx59-headphones"},
            {"slug": "zx9-speaker"}
        ],
        "categoryOrder": 1
    },
{
    "slug": "xx99-mark-one-headphones",
    "category": "headphones",
    "categoryLabel": "Headphones",
    "shortName": "XX99 MK I",
    "name": "XX99 Mark I Headphones",
    "price": 1750,
    "description":
      "As the gold standard for headphones, the classic XX99 Mark I offers detailed and accurate audio reproduction for audiophiles, mixing engineers, and music lovers alike in studios and on the go.",
    "features": [
      "Built for critical listening, the XX99 Mark I uses high-output drivers with a refined acoustic chamber to reveal every nuance in your music. The robust construction and cushioned ear pads make it ideal for long sessions without fatigue.",
      "With its dependable wired connection and balanced tuning, it remains a trusted reference pair for creators and enthusiasts who want a reliable premium experience at home or in the studio.",
    ],
    "includes": [
      { "quantity": 1, "item": "Headphone unit" },
      { "quantity": 2, "item": "Replacement earcups" },
      { "quantity": 1, "item": "User manual" },
      { "quantity": 1, "item": "3.5mm 5m audio cable" },
    ],
    "categoryImage": {
      "mobile":
        "/assets/product-xx99-mark-one-headphones/mobile/image-category-page-preview.jpg",
      "tablet":
        "/assets/product-xx99-mark-one-headphones/tablet/image-category-page-preview.jpg",
      "desktop":
        "/assets/product-xx99-mark-one-headphones/desktop/image-category-page-preview.jpg",
    },
    "productImage": {
      "mobile": "/assets/product-xx99-mark-one-headphones/mobile/image-product.jpg",
      "tablet": "/assets/product-xx99-mark-one-headphones/tablet/image-product.jpg",
      "desktop": "/assets/product-xx99-mark-one-headphones/desktop/image-product.jpg",
    },
    "gallery": {
      "first": {
        "mobile":
          "/assets/product-xx99-mark-one-headphones/mobile/image-gallery-1.jpg",
        "tablet":
          "/assets/product-xx99-mark-one-headphones/tablet/image-gallery-1.jpg",
        "desktop":
          "/assets/product-xx99-mark-one-headphones/desktop/image-gallery-1.jpg",
      },
      "second": {
        "mobile":
          "/assets/product-xx99-mark-one-headphones/mobile/image-gallery-2.jpg",
        "tablet":
          "/assets/product-xx99-mark-one-headphones/tablet/image-gallery-2.jpg",
        "desktop":
          "/assets/product-xx99-mark-one-headphones/desktop/image-gallery-2.jpg",
      },
      "third": {
        "mobile":
          "/assets/product-xx99-mark-one-headphones/mobile/image-gallery-3.jpg",
        "tablet":
          "/assets/product-xx99-mark-one-headphones/tablet/image-gallery-3.jpg",
        "desktop":
          "/assets/product-xx99-mark-one-headphones/desktop/image-gallery-3.jpg",
      },
    },
    "others": [
      {
        "slug": "xx99-mark-two-headphones",
        "category": "headphones",
        "name": "XX99 Mark II",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx99-mark-two-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx99-mark-two-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx99-mark-two-headphones.jpg",
        },
      },
      {
        "slug": "xx59-headphones",
        "category": "headphones",
        "name": "XX59",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx59-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx59-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx59-headphones.jpg",
        },
      },
      {
        "slug": "zx9-speaker",
        "category": "speakers",
        "name": "ZX9 Speaker",
        "image": {
          "mobile": "/assets/shared/mobile/image-zx9-speaker.jpg",
          "tablet": "/assets/shared/tablet/image-zx9-speaker.jpg",
          "desktop": "/assets/shared/desktop/image-zx9-speaker.jpg",
        },
      },
    ],
    "categoryOrder": 2,
  },
  {
    "slug": "xx59-headphones",
    "category": "headphones",
    "categoryLabel": "Headphones",
    "shortName": "XX59",
    "name": "XX59 Headphones",
    "price": 899,
    "description":
      "Enjoy your audio almost anywhere and customize it to your specific tastes with the XX59 headphones. The stylish yet durable design provides a dependable premium experience at a more accessible price point.",
    "features": [
      "The XX59 packs a punch with a lively presentation and strong bass response that makes everyday listening enjoyable across genres. Lightweight materials and a secure fit help it stay comfortable throughout the day.",
      "Its clean industrial styling and robust build make it a dependable entry into the Audiophile range, delivering quality sound and thoughtful ergonomics in one affordable package.",
    ],
    "includes": [
      { "quantity": 1, "item": "Headphone unit" },
      { "quantity": 2, "item": "Replacement earcups" },
      { "quantity": 1, "item": "User manual" },
      { "quantity": 1, "item": "3.5mm 5m audio cable" },
    ],
    "categoryImage": {
      "mobile":
        "/assets/product-xx59-headphones/mobile/image-category-page-preview.jpg",
      "tablet":
        "/assets/product-xx59-headphones/tablet/image-category-page-preview.jpg",
      "desktop":
        "/assets/product-xx59-headphones/desktop/image-category-page-preview.jpg",
    },
    "productImage": {
      "mobile": "/assets/product-xx59-headphones/mobile/image-product.jpg",
      "tablet": "/assets/product-xx59-headphones/tablet/image-product.jpg",
      "desktop": "/assets/product-xx59-headphones/desktop/image-product.jpg",
    },
    "gallery": {
      "first": {
        "mobile": "/assets/product-xx59-headphones/mobile/image-gallery-1.jpg",
        "tablet": "/assets/product-xx59-headphones/tablet/image-gallery-1.jpg",
        "desktop": "/assets/product-xx59-headphones/desktop/image-gallery-1.jpg",
      },
      "second": {
        "mobile": "/assets/product-xx59-headphones/mobile/image-gallery-2.jpg",
        "tablet": "/assets/product-xx59-headphones/tablet/image-gallery-2.jpg",
        "desktop": "/assets/product-xx59-headphones/desktop/image-gallery-2.jpg",
      },
      "third": {
        "mobile": "/assets/product-xx59-headphones/mobile/image-gallery-3.jpg",
        "tablet": "/assets/product-xx59-headphones/tablet/image-gallery-3.jpg",
        "desktop": "/assets/product-xx59-headphones/desktop/image-gallery-3.jpg",
      },
    },
    "others": [
      {
        "slug": "xx99-mark-two-headphones",
        "category": "headphones",
        "name": "XX99 Mark II",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx99-mark-two-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx99-mark-two-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx99-mark-two-headphones.jpg",
        },
      },
      {
        "slug": "xx99-mark-one-headphones",
        "category": "headphones",
        "name": "XX99 Mark I",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx99-mark-one-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx99-mark-one-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx99-mark-one-headphones.jpg",
        },
      },
      {
        "slug": "zx9-speaker",
        "category": "speakers",
        "name": "ZX9 Speaker",
        "image": {
          "mobile": "/assets/shared/mobile/image-zx9-speaker.jpg",
          "tablet": "/assets/shared/tablet/image-zx9-speaker.jpg",
          "desktop": "/assets/shared/desktop/image-zx9-speaker.jpg",
        },
      },
    ],
    "categoryOrder": 3,
  },
  {
    "slug": "zx9-speaker",
    "category": "speakers",
    "categoryLabel": "Speakers",
    "shortName": "ZX9",
    "name": "ZX9 Speaker",
    "isNew": True,
    "price": 4500,
    "description":
      "Upgrade your sound system with the all new ZX9 active speaker. It is a bookshelf speaker system that offers truly remarkable high-fidelity performance and enough connectivity to become the center of your setup.",
    "features": [
      "Connect via Bluetooth or nearly any wired source with confidence. The ZX9 uses premium internal components and a carefully tuned cabinet to produce deep bass, detailed mids, and sparkling highs without distortion at higher volumes.",
      "Its commanding presence and versatile connectivity make it equally comfortable in a living room, studio, or dedicated listening space, delivering powerful room-filling audio with refined control.",
    ],
    "includes": [
      { "quantity": 2, "item": "Speaker unit" },
      { "quantity": 2, "item": "Speaker cloth panel" },
      { "quantity": 1, "item": "User manual" },
      { "quantity": 1, "item": "3.5mm 10m audio cable" },
      { "quantity": 1, "item": "10m optical cable" },
    ],
    "categoryImage": {
      "mobile":
        "/assets/product-zx9-speaker/mobile/image-category-page-preview.jpg",
      "tablet":
        "/assets/product-zx9-speaker/tablet/image-category-page-preview.jpg",
      "desktop":
        "/assets/product-zx9-speaker/desktop/image-category-page-preview.jpg",
    },
    "productImage": {
      "mobile": "/assets/product-zx9-speaker/mobile/image-product.jpg",
      "tablet": "/assets/product-zx9-speaker/tablet/image-product.jpg",
      "desktop": "/assets/product-zx9-speaker/desktop/image-product.jpg",
    },
    "gallery": {
      "first": {
        "mobile": "/assets/product-zx9-speaker/mobile/image-gallery-1.jpg",
        "tablet": "/assets/product-zx9-speaker/tablet/image-gallery-1.jpg",
        "desktop": "/assets/product-zx9-speaker/desktop/image-gallery-1.jpg",
      },
      "second": {
        "mobile": "/assets/product-zx9-speaker/mobile/image-gallery-2.jpg",
        "tablet": "/assets/product-zx9-speaker/tablet/image-gallery-2.jpg",
        "desktop": "/assets/product-zx9-speaker/desktop/image-gallery-2.jpg",
      },
    "third": {
        "mobile": "/assets/product-zx9-speaker/mobile/image-gallery-3.jpg",
        "tablet": "/assets/product-zx9-speaker/tablet/image-gallery-3.jpg",
        "desktop": "/assets/product-zx9-speaker/desktop/image-gallery-3.jpg",
      },
    },
    "others": [
      {
        "slug": "zx7-speaker",
        "category": "speakers",
        "name": "ZX7 Speaker",
        "image": {
          "mobile": "/assets/shared/mobile/image-zx7-speaker.jpg",
          "tablet": "/assets/shared/tablet/image-zx7-speaker.jpg",
          "desktop": "/assets/shared/desktop/image-zx7-speaker.jpg",
        },
      },
      {
        "slug": "xx99-mark-one-headphones",
        "category": "headphones",
        "name": "XX99 Mark I",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx99-mark-one-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx99-mark-one-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx99-mark-one-headphones.jpg",
        },
      },
      {
        "slug": "xx59-headphones",
        "category": "headphones",
        "name": "XX59",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx59-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx59-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx59-headphones.jpg",
        },
      },
    ],
    "categoryOrder": 1,
  },
  {
    "slug": "zx7-speaker",
    "category": "speakers",
    "categoryLabel": "Speakers",
    "shortName": "ZX7",
    "name": "ZX7 Speaker",
    "price": 3500,
    "description":
      "Stream high quality sound wirelessly with minimal loss using the ZX7 bookshelf speaker. It uses advanced drivers and premium amplification to deliver natural, room-filling audio for everyday listening.",
    "features": [
      "The ZX7 combines a compact footprint with a powerful acoustic signature, making it a strong option for modern setups that need performance without overwhelming the room. Rich mids and articulate detail give vocals and instruments a convincing presence.",
      "Its understated design allows it to blend seamlessly into a wide variety of interiors while still offering the premium finish and sound quality expected from the Audiophile lineup.",
    ],
    "includes": [
      { "quantity": 2, "item": "Speaker unit" },
      { "quantity": 2, "item": "Speaker cloth panel" },
      { "quantity": 1, "item": "User manual" },
      { "quantity": 1, "item": "3.5mm 7.5m audio cable" },
      { "quantity": 1, "item": "7.5m optical cable" },
    ],
    "categoryImage": {
      "mobile":
        "/assets/product-zx7-speaker/mobile/image-category-page-preview.jpg",
      "tablet":
        "/assets/product-zx7-speaker/tablet/image-category-page-preview.jpg",
      "desktop":
        "/assets/product-zx7-speaker/desktop/image-category-page-preview.jpg",
    },
    "productImage": {
      "mobile": "/assets/product-zx7-speaker/mobile/image-product.jpg",
      "tablet": "/assets/product-zx7-speaker/tablet/image-product.jpg",
      "desktop": "/assets/product-zx7-speaker/desktop/image-product.jpg",
    },
    "gallery": {
      "first": {
        "mobile": "/assets/product-zx7-speaker/mobile/image-gallery-1.jpg",
        "tablet": "/assets/product-zx7-speaker/tablet/image-gallery-1.jpg",
        "desktop": "/assets/product-zx7-speaker/desktop/image-gallery-1.jpg",
      },
      "second": {
        "mobile": "/assets/product-zx7-speaker/mobile/image-gallery-2.jpg",
        "tablet": "/assets/product-zx7-speaker/tablet/image-gallery-2.jpg",
        "desktop": "/assets/product-zx7-speaker/desktop/image-gallery-2.jpg",
      },
      "third": {
        "mobile": "/assets/product-zx7-speaker/mobile/image-gallery-3.jpg",
        "tablet": "/assets/product-zx7-speaker/tablet/image-gallery-3.jpg",
        "desktop": "/assets/product-zx7-speaker/desktop/image-gallery-3.jpg",
      },
    },
    "others": [
      {
        "slug": "zx9-speaker",
        "category": "speakers",
        "name": "ZX9 Speaker",
        "image": {
          "mobile": "/assets/shared/mobile/image-zx9-speaker.jpg",
          "tablet": "/assets/shared/tablet/image-zx9-speaker.jpg",
          "desktop": "/assets/shared/desktop/image-zx9-speaker.jpg",
        },
      },
      {
        "slug": "xx99-mark-two-headphones",
        "category": "headphones",
        "name": "XX99 Mark II",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx99-mark-two-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx99-mark-two-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx99-mark-two-headphones.jpg",
        },
      },
      {
        "slug": "yx1-earphones",
        "category": "earphones",
        "name": "YX1 Earphones",
        "image": {
          "mobile": "/assets/product-yx1-earphones/mobile/image-product.jpg",
          "tablet": "/assets/product-yx1-earphones/tablet/image-product.jpg",
          "desktop": "/assets/product-yx1-earphones/desktop/image-product.jpg",
        },
      },
    ],
    "categoryOrder": 2,
  },
  {
    "slug": "yx1-earphones",
    "category": "earphones",
    "categoryLabel": "Earphones",
    "shortName": "YX1",
    "name": "YX1 Wireless Earphones",
    "price": 599,
    "description":
      "Tailor your listening experience with bespoke dynamic drivers from the new YX1 wireless earphones. Enjoy incredible high-fidelity sound even in noisy environments with its advanced active noise cancellation.",
    "features": [
      "Experience unrivaled stereo sound thanks to innovative acoustic technology with a rich, full-bodied presentation. The ergonomically shaped housings create a secure fit that is comfortable enough for extended sessions, workouts, and commutes alike.",
      "The charging case adds convenience on the move while the wireless design removes cable clutter entirely, making the YX1 an easy everyday upgrade for listeners who want portability without sacrificing premium detail.",
    ],
    "includes": [
      { "quantity": 2, "item": "Earphone unit" },
      { "quantity": 6, "item": "Multi-size earplugs" },
      { "quantity": 1, "item": "User manual" },
      { "quantity": 1, "item": "USB-C charging cable" },
      { "quantity": 1, "item": "Travel pouch" },
    ],
    "categoryImage": {
      "mobile":
        "/assets/product-yx1-earphones/mobile/image-category-page-preview.jpg",
      "tablet":
        "/assets/product-yx1-earphones/tablet/image-category-page-preview.jpg",
      "desktop":
        "/assets/product-yx1-earphones/desktop/image-category-page-preview.jpg",
    },
    "productImage": {
      "mobile": "/assets/product-yx1-earphones/mobile/image-product.jpg",
      "tablet": "/assets/product-yx1-earphones/tablet/image-product.jpg",
      "desktop": "/assets/product-yx1-earphones/desktop/image-product.jpg",
    },
    "gallery": {
      "first": {
        "mobile": "/assets/product-yx1-earphones/mobile/image-gallery-1.jpg",
        "tablet": "/assets/product-yx1-earphones/tablet/image-gallery-1.jpg",
        "desktop": "/assets/product-yx1-earphones/desktop/image-gallery-1.jpg",
      },
      "second": {
        "mobile": "/assets/product-yx1-earphones/mobile/image-gallery-2.jpg",
        "tablet": "/assets/product-yx1-earphones/tablet/image-gallery-2.jpg",
        "desktop": "/assets/product-yx1-earphones/desktop/image-gallery-2.jpg",
      },
      "third": {
        "mobile": "/assets/product-yx1-earphones/mobile/image-gallery-3.jpg",
        "tablet": "/assets/product-yx1-earphones/tablet/image-gallery-3.jpg",
        "desktop": "/assets/product-yx1-earphones/desktop/image-gallery-3.jpg",
      },
    },
    "others": [
      {
        "slug": "xx99-mark-one-headphones",
        "category": "headphones",
        "name": "XX99 Mark I",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx99-mark-one-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx99-mark-one-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx99-mark-one-headphones.jpg",
        },
      },
      {
        "slug": "xx59-headphones",
        "category": "headphones",
        "name": "XX59",
        "image": {
          "mobile": "/assets/shared/mobile/image-xx59-headphones.jpg",
          "tablet": "/assets/shared/tablet/image-xx59-headphones.jpg",
          "desktop": "/assets/shared/desktop/image-xx59-headphones.jpg",
        },
      },
      {
        "slug": "zx9-speaker",
        "category": "speakers",
        "name": "ZX9 Speaker",
        "image": {
          "mobile": "/assets/shared/mobile/image-zx9-speaker.jpg",
          "tablet": "/assets/shared/tablet/image-zx9-speaker.jpg",
          "desktop": "/assets/shared/desktop/image-zx9-speaker.jpg",
        },
      },
    ],
    "categoryOrder": 1,
  },
]

# Insert each product into 'products' table safely
for p in products:
  if not isinstance(p, dict):
    print(f"Skipping invalid product: {p}")
    continue  # skip if product is not a dictionary

  # Safe extraction with defaults
  slug = p.get("slug", None)
  name = p.get("name", "Unnamed Product")
  short_name = p.get("shortName", "")
  category = p.get("category", "")
  category_label = p.get("categoryLabel", "")
  is_new = p.get("isNew", False)
  price = p.get("price", 0)
  description = p.get("description", "")
  category_order = p.get("categoryOrder", 0)

  # Insert product and get product_id
  cur.execute("""
        INSERT INTO products 
        (slug, name, short_name, category, category_label, is_new, price, description, category_order)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (slug, name, short_name, category, category_label, is_new, price, description, category_order))

  product_id = cur.fetchone()[0]

  # Insert features safely
  features = p.get("features", [])
  if isinstance(features, list):
    for feature in features:
      if isinstance(feature, str):
        cur.execute("INSERT INTO features (product_id, feature) VALUES (%s, %s)", (product_id, feature))

  # Insert includes safely
  includes = p.get("includes", [])
  if isinstance(includes, list):
    for include in includes:
      if isinstance(include, dict):
        item = include.get("item", "Unknown")
        quantity = include.get("quantity", 1)
        cur.execute("INSERT INTO includes (product_id, item, quantity) VALUES (%s, %s, %s)",
                    (product_id, item, quantity))

  # Insert category images safely
  category_images = p.get("categoryImage", {})
  if isinstance(category_images, dict):
    for device, url in category_images.items():
      if isinstance(device, str) and isinstance(url, str):
        cur.execute("INSERT INTO product_images (product_id, device, context, url) VALUES (%s, %s, %s, %s)",
                    (product_id, device, "category", url))

  # Insert product images safely
  product_images = p.get("productImage", {})
  if isinstance(product_images, dict):
    for device, url in product_images.items():
      if isinstance(device, str) and isinstance(url, str):
        cur.execute("INSERT INTO product_images (product_id, device, context, url) VALUES (%s, %s, %s, %s)",
                    (product_id, device, "product", url))

  # Insert gallery images safely
  gallery = p.get("gallery", {})
  if isinstance(gallery, dict):
    for idx, gallery_key in enumerate(["first", "second", "third"], start=1):
      images = gallery.get(gallery_key, {})
      if isinstance(images, dict):
        for device, url in images.items():
          if isinstance(device, str) and isinstance(url, str):
            context = f"gallery_{idx}"
            cur.execute("INSERT INTO product_images (product_id, device, context, url) VALUES (%s, %s, %s, %s)",
                        (product_id, device, context, url))

  # Insert related products safely
  for p in products:
    if not isinstance(p, dict):
      continue

  cur.execute("SELECT id FROM products WHERE slug = %s", (p.get("slug", ""),))
  result = cur.fetchone()
  if not result:
    continue
  product_id = result[0]

  others = p.get("others", [])
  if isinstance(others, list):
    for other in others:
      if isinstance(other, dict):
        cur.execute("SELECT id FROM products WHERE slug = %s", (other.get("slug", ""),))
        related = cur.fetchone()
        if related:
          related_product_id = related[0]
          cur.execute("INSERT INTO related_products (product_id, related_product_id) VALUES (%s, %s)",
                      (product_id, related_product_id))

# Commit all changes and close connection
conn.commit()
cur.close()
conn.close()
print("Products, features, includes, images, and related products inserted successfully!")