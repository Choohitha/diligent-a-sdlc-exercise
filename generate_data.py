"""
Script to generate synthetic ecommerce data.
This script creates 5 CSV files with realistic ecommerce data.
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Configuration
NUM_CUSTOMERS = 100
NUM_PRODUCTS = 80
NUM_ORDERS = 150
NUM_SUPPLIERS = 15

# Create data directory
import os
os.makedirs('data', exist_ok=True)

# Categories for products
CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports', 'Toys', 'Beauty', 'Food & Beverages']

# Order statuses
ORDER_STATUSES = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']

# Generate Suppliers
suppliers = []
for i in range(1, NUM_SUPPLIERS + 1):
    suppliers.append({
        'supplier_id': i,
        'supplier_name': fake.company(),
        'contact_email': fake.company_email(),
        'phone': fake.phone_number(),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state_abbr()
    })

# Write suppliers.csv
with open('data/suppliers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['supplier_id', 'supplier_name', 'contact_email', 'phone', 'address', 'city', 'state'])
    writer.writeheader()
    writer.writerows(suppliers)

print(f"Generated {NUM_SUPPLIERS} suppliers")

# Generate Products
products = []
for i in range(1, NUM_PRODUCTS + 1):
    products.append({
        'product_id': i,
        'product_name': fake.catch_phrase() + ' ' + random.choice(['Pro', 'Premium', 'Basic', 'Deluxe', 'Standard']),
        'category': random.choice(CATEGORIES),
        'price': round(random.uniform(9.99, 999.99), 2),
        'stock_quantity': random.randint(0, 500),
        'description': fake.text(max_nb_chars=200),
        'supplier_id': random.randint(1, NUM_SUPPLIERS)
    })

# Write products.csv
with open('data/products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_id', 'product_name', 'category', 'price', 'stock_quantity', 'description', 'supplier_id'])
    writer.writeheader()
    writer.writerows(products)

print(f"Generated {NUM_PRODUCTS} products")

# Generate Customers
customers = []
start_date = datetime.now() - timedelta(days=730)  # 2 years ago
for i in range(1, NUM_CUSTOMERS + 1):
    reg_date = fake.date_between(start_date=start_date, end_date='today')
    customers.append({
        'customer_id': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state_abbr(),
        'zip_code': fake.zipcode(),
        'registration_date': reg_date.strftime('%Y-%m-%d')
    })

# Write customers.csv
with open('data/customers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['customer_id', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'registration_date'])
    writer.writeheader()
    writer.writerows(customers)

print(f"Generated {NUM_CUSTOMERS} customers")

# Generate Orders
orders = []
order_items = []
order_item_id = 1

for i in range(1, NUM_ORDERS + 1):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    order_date = fake.date_between(start_date=start_date, end_date='today')
    status = random.choice(ORDER_STATUSES)
    
    # Generate 1-5 items per order
    num_items = random.randint(1, 5)
    total_amount = 0
    
    for _ in range(num_items):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = product['price']
        subtotal = round(quantity * unit_price, 2)
        total_amount += subtotal
        
        order_items.append({
            'order_item_id': order_item_id,
            'order_id': i,
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': subtotal
        })
        order_item_id += 1
    
    orders.append({
        'order_id': i,
        'customer_id': customer_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'total_amount': round(total_amount, 2),
        'status': status,
        'shipping_address': fake.street_address()
    })

# Write orders.csv
with open('data/orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'customer_id', 'order_date', 'total_amount', 'status', 'shipping_address'])
    writer.writeheader()
    writer.writerows(orders)

print(f"Generated {NUM_ORDERS} orders")

# Write order_items.csv
with open('data/order_items.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'subtotal'])
    writer.writeheader()
    writer.writerows(order_items)

print(f"Generated {len(order_items)} order items")
print("\nAll data files generated successfully in the 'data' directory!")

