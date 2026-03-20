import psycopg2

# Connect to PostgresSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="okanmife@07",
    port=5432
)

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Drop tables if they already exist (clears old data)
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

# Create 'features' table (product that has multiple features)
cur.execute("""
CREATE TABLE IF NOT EXISTS features (
  id SERIAL PRIMARY KEY,
  product_id INT REFERENCES products(id) ON DELETE CASCADE,
  feature TEXT
)
""")

# Create 'includes' table (what comes with the product)
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

# Create 'related_products' table (cross-reference related products)
cur.execute("""
CREATE TABLE IF NOT EXISTS related_products (
  id SERIAL PRIMARY KEY,
  product_id INT REFERENCES products(id) ON DELETE CASCADE,
  related_product_id INT REFERENCES products(id) ON DELETE CASCADE
);
""")

# Commit all changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()