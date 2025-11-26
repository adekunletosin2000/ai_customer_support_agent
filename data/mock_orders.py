"""
Mock data generator for e-commerce orders
Creates 20 realistic order records in the database
"""
import sqlite3
import random
from datetime import datetime, timedelta

# Create database connection
conn = sqlite3.connect('data/ecommerce.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    customer_name TEXT,
    customer_email TEXT,
    order_date TEXT,
    status TEXT,
    total_amount REAL,
    shipping_address TEXT,
    tracking_number TEXT,
    last_scan_location TEXT,
    estimated_delivery TEXT,
    items TEXT
)
''')

# Sample data
statuses = ["Processing", "Shipped", "In Transit", "Out for Delivery", "Delivered", "Delayed"]
cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
products = [
    "Wireless Headphones",
    "Smart Watch",
    "Phone Case",
    "Laptop Bag",
    "USB-C Cable",
    "Power Bank",
    "Bluetooth Speaker",
    "Fitness Tracker",
    "Phone Charger",
    "Screen Protector"
]

names = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Rohan", "Kavya", "Arjun", "Ishaan"]
lastnames = ["Sharma", "Patel", "Kumar", "Singh", "Reddy", "Gupta", "Mehta", "Shah", "Iyer", "Joshi"]

# Generate 20 orders
orders_data = []
for i in range(1, 21):
    order_id = f"ORD{12340 + i}"
    customer_id = f"C{1000 + i}"
    
    first_name = random.choice(names)
    last_name = random.choice(lastnames)
    customer_name = f"{first_name} {last_name}"
    customer_email = f"{first_name.lower()}.{last_name.lower()}@email.com"
    
    # Random date in last 30 days
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
    
    status = random.choice(statuses)
    total_amount = round(random.uniform(500, 5000), 2)
    
    city = random.choice(cities)
    shipping_address = f"{random.randint(1, 999)}, {random.choice(['MG Road', 'Park Street', 'Main Road', 'Nehru Place'])}, {city}"
    
    tracking_number = f"TRK{1000000 + i}"
    last_scan_location = f"{city} Distribution Center"
    
    # Estimated delivery 2-7 days from order date
    est_delivery = (datetime.strptime(order_date, '%Y-%m-%d') + timedelta(days=random.randint(2, 7))).strftime('%Y-%m-%d')
    
    # Random items (1-3 products)
    num_items = random.randint(1, 3)
    items = ", ".join(random.sample(products, num_items))
    
    orders_data.append((
        order_id, customer_id, customer_name, customer_email,
        order_date, status, total_amount, shipping_address,
        tracking_number, last_scan_location, est_delivery, items
    ))

# Insert data
cursor.executemany('''
    INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', orders_data)

conn.commit()
print(f"✅ Successfully created {len(orders_data)} orders in database")

# Print sample
cursor.execute("SELECT order_id, customer_name, status, items FROM orders LIMIT 5")
print("\n📦 Sample Orders:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} - {row[2]} ({row[3]})")

conn.close()
