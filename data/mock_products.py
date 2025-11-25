"""
Mock data generator for e-commerce products
Creates 20 product records in the database
"""
import sqlite3

# Create database connection
conn = sqlite3.connect('data/ecommerce.db')
cursor = conn.cursor()

# Create products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    description TEXT,
    in_stock BOOLEAN,
    image_url TEXT,
    rating REAL
)
''')

# Product data
products_data = [
    ("P001", "Wireless Bluetooth Headphones", "Electronics", 2999.00, "Premium noise-cancelling over-ear headphones with 30hr battery", True, "headphones.jpg", 4.5),
    ("P002", "Smart Fitness Watch", "Wearables", 4999.00, "Track your health with heart rate monitor, GPS, and sleep tracking", True, "smartwatch.jpg", 4.3),
    ("P003", "Leather Phone Case", "Accessories", 499.00, "Genuine leather case compatible with latest smartphones", True, "phonecase.jpg", 4.7),
    ("P004", "Professional Laptop Bag", "Bags", 1899.00, "Water-resistant laptop bag with multiple compartments", True, "laptopbag.jpg", 4.4),
    ("P005", "USB-C Fast Charging Cable", "Electronics", 299.00, "3-meter Type-C cable supports fast charging", True, "cable.jpg", 4.6),
    ("P006", "20000mAh Power Bank", "Electronics", 1499.00, "High capacity power bank with dual USB output", True, "powerbank.jpg", 4.5),
    ("P007", "Portable Bluetooth Speaker", "Electronics", 2499.00, "Waterproof speaker with 360° sound and 12hr playtime", True, "speaker.jpg", 4.8),
    ("P008", "Fitness Resistance Bands", "Sports", 699.00, "Set of 5 resistance bands for home workouts", True, "bands.jpg", 4.2),
    ("P009", "Wireless Phone Charger", "Electronics", 899.00, "10W fast wireless charging pad", True, "charger.jpg", 4.4),
    ("P010", "Tempered Glass Screen Protector", "Accessories", 199.00, "9H hardness screen protector with oleophobic coating", True, "screenprotector.jpg", 4.1),
    ("P011", "Gaming Mouse", "Electronics", 1599.00, "RGB gaming mouse with 12000 DPI", True, "mouse.jpg", 4.6),
    ("P012", "Yoga Mat", "Sports", 899.00, "Non-slip 6mm thick yoga mat with carrying strap", True, "yogamat.jpg", 4.5),
    ("P013", "Water Bottle", "Accessories", 399.00, "1L stainless steel insulated water bottle", True, "bottle.jpg", 4.3),
    ("P014", "Notebook Set", "Stationery", 599.00, "Pack of 3 premium ruled notebooks", True, "notebook.jpg", 4.7),
    ("P015", "Desk Lamp", "Home", 1299.00, "LED desk lamp with adjustable brightness", True, "lamp.jpg", 4.4),
    ("P016", "Running Shoes", "Footwear", 3499.00, "Lightweight running shoes with superior cushioning", False, "shoes.jpg", 4.8),
    ("P017", "Sunglasses", "Accessories", 1199.00, "UV protection polarized sunglasses", True, "sunglasses.jpg", 4.2),
    ("P018", "Backpack", "Bags", 2199.00, "30L travel backpack with laptop compartment", True, "backpack.jpg", 4.6),
    ("P019", "Coffee Mug", "Home", 299.00, "Ceramic coffee mug with lid", True, "mug.jpg", 4.5),
    ("P020", "Wireless Mouse", "Electronics", 699.00, "Ergonomic wireless mouse with silent clicks", True, "wirelessmouse.jpg", 4.4),
]

# Insert data
cursor.executemany('''
    INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', products_data)

conn.commit()
print(f"✅ Successfully created {len(products_data)} products in database")

# Print sample
cursor.execute("SELECT product_id, name, price, in_stock FROM products LIMIT 5")
print("\n🛍️ Sample Products:")
for row in cursor.fetchall():
    stock_status = "In Stock" if row[3] else "Out of Stock"
    print(f"  {row[0]}: {row[1]} - ₹{row[2]} ({stock_status})")

conn.close()
