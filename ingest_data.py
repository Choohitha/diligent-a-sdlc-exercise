"""
Script to ingest CSV data into SQLite database.
This script reads the generated CSV files and loads them into a SQLite database.
"""

import sqlite3
import csv
import os
from datetime import datetime

DB_NAME = 'ecommerce.db'
DATA_DIR = 'data'

# CSV files and their corresponding table names
CSV_FILES = {
    'suppliers.csv': 'suppliers',
    'products.csv': 'products',
    'customers.csv': 'customers',
    'orders.csv': 'orders',
    'order_items.csv': 'order_items'
}

def create_tables(cursor):
    """Create all necessary tables in the database."""
    
    # Drop tables if they exist (for clean re-runs)
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS suppliers")
    
    # Create suppliers table
    cursor.execute("""
        CREATE TABLE suppliers (
            supplier_id INTEGER PRIMARY KEY,
            supplier_name TEXT NOT NULL,
            contact_email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT
        )
    """)
    
    # Create products table
    cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock_quantity INTEGER,
            description TEXT,
            supplier_id INTEGER,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        )
    """)
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            registration_date TEXT
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            total_amount REAL,
            status TEXT,
            shipping_address TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # Create order_items table
    cursor.execute("""
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            subtotal REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    
    print("Database tables created successfully!")

def ingest_csv_to_table(conn, cursor, csv_file, table_name):
    """Read a CSV file and insert its data into the corresponding table."""
    file_path = os.path.join(DATA_DIR, csv_file)
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Skipping...")
        return 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if not rows:
                print(f"No data found in {csv_file}")
                return 0
            
            # Get column names from CSV
            columns = reader.fieldnames
            
            # Create placeholders for INSERT statement
            placeholders = ','.join(['?' for _ in columns])
            columns_str = ','.join(columns)
            
            # Prepare INSERT statement
            insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            # Insert rows
            count = 0
            for row in rows:
                values = [row[col] for col in columns]
                cursor.execute(insert_sql, values)
                count += 1
            
            conn.commit()
            print(f"  [OK] Inserted {count} records into {table_name}")
            return count
            
    except Exception as e:
        print(f"  [ERROR] Error inserting data into {table_name}: {str(e)}")
        conn.rollback()
        return 0

def main():
    """Main function to orchestrate the data ingestion."""
    print("Starting data ingestion into SQLite database...")
    print(f"Database: {DB_NAME}")
    print(f"Data directory: {DATA_DIR}\n")
    
    # Connect to SQLite database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Create tables
        create_tables(cursor)
        print()
        
        # Ingest data in order (respecting foreign key constraints)
        ingestion_order = ['suppliers.csv', 'customers.csv', 'products.csv', 'orders.csv', 'order_items.csv']
        
        total_records = 0
        for csv_file in ingestion_order:
            if csv_file in CSV_FILES:
                table_name = CSV_FILES[csv_file]
                count = ingest_csv_to_table(conn, cursor, csv_file, table_name)
                total_records += count
        
        print(f"\n{'='*50}")
        print(f"Data ingestion completed!")
        print(f"Total records inserted: {total_records}")
        print(f"Database file: {DB_NAME}")
        print(f"{'='*50}")
        
        # Display table statistics
        print("\nTable Statistics:")
        for table_name in CSV_FILES.values():
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  {table_name}: {count} records")
        
    except Exception as e:
        print(f"\nError during data ingestion: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()

