"""
Script to execute SQL queries with multiple table joins.
This script demonstrates complex SQL queries joining multiple tables from the ecommerce database.
"""

import sqlite3
import csv
from datetime import datetime

DB_NAME = 'ecommerce.db'

def execute_query_and_display(cursor, query, description):
    """Execute a SQL query and display results in a formatted way."""
    print(f"\n{'='*80}")
    print(f"QUERY: {description}")
    print(f"{'='*80}")
    print(f"\nSQL Query:\n{query}\n")
    print(f"{'-'*80}")
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        if not results:
            print("No results found.")
            return results
        
        # Calculate column widths
        col_widths = [len(col) for col in column_names]
        for row in results:
            for i, value in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(value)))
        
        # Print header
        header = " | ".join(str(col).ljust(col_widths[i]) for i, col in enumerate(column_names))
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in results:
            row_str = " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
            print(row_str)
        
        print(f"\nTotal rows: {len(results)}")
        return results
        
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return None

def export_to_csv(results, column_names, filename):
    """Export query results to a CSV file."""
    if not results:
        print("No data to export.")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            writer.writerows(results)
        print(f"\nResults exported to {filename}")
    except Exception as e:
        print(f"Error exporting to CSV: {str(e)}")

def main():
    """Main function to execute various SQL queries."""
    print("Ecommerce Database - SQL Query Analysis")
    print("=" * 80)
    
    # Connect to database
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        print(f"Connected to database: {DB_NAME}\n")
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return
    
    try:
        # Query 1: Detailed Order History with Customer and Product Information
        query1 = """
        SELECT 
            o.order_id,
            o.order_date,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email AS customer_email,
            p.product_name,
            p.category,
            oi.quantity,
            oi.unit_price,
            oi.subtotal,
            o.total_amount AS order_total,
            o.status AS order_status
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        ORDER BY o.order_date DESC, o.order_id
        LIMIT 50
        """
        
        results1 = execute_query_and_display(cursor, query1, 
            "Detailed Order History (Customers, Orders, Order Items, Products)")
        
        # Export first query to CSV
        if results1:
            column_names1 = [desc[0] for desc in cursor.description]
            export_to_csv(results1, column_names1, 'output_detailed_orders.csv')
        
        # Query 2: Sales Performance by Product Category
        query2 = """
        SELECT 
            p.category,
            COUNT(DISTINCT oi.order_id) AS total_orders,
            SUM(oi.quantity) AS total_quantity_sold,
            SUM(oi.subtotal) AS total_revenue,
            AVG(oi.unit_price) AS avg_price,
            COUNT(DISTINCT p.product_id) AS unique_products
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status != 'Cancelled'
        GROUP BY p.category
        ORDER BY total_revenue DESC
        """
        
        results2 = execute_query_and_display(cursor, query2,
            "Sales Performance by Product Category")
        
        if results2:
            column_names2 = [desc[0] for desc in cursor.description]
            export_to_csv(results2, column_names2, 'output_category_sales.csv')
        
        # Query 3: Top Customers by Total Spending
        query3 = """
        SELECT 
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email,
            c.city || ', ' || c.state AS location,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(o.total_amount) AS total_spent,
            AVG(o.total_amount) AS avg_order_value,
            MAX(o.order_date) AS last_order_date
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status != 'Cancelled'
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state
        ORDER BY total_spent DESC
        LIMIT 20
        """
        
        results3 = execute_query_and_display(cursor, query3,
            "Top 20 Customers by Total Spending")
        
        if results3:
            column_names3 = [desc[0] for desc in cursor.description]
            export_to_csv(results3, column_names3, 'output_top_customers.csv')
        
        # Query 4: Supplier Performance with Product Sales
        query4 = """
        SELECT 
            s.supplier_id,
            s.supplier_name,
            s.city || ', ' || s.state AS supplier_location,
            COUNT(DISTINCT p.product_id) AS products_supplied,
            COUNT(DISTINCT oi.order_id) AS orders_with_products,
            SUM(oi.quantity) AS total_units_sold,
            SUM(oi.subtotal) AS total_revenue,
            AVG(oi.unit_price) AS avg_selling_price
        FROM suppliers s
        JOIN products p ON s.supplier_id = p.supplier_id
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status != 'Cancelled'
        GROUP BY s.supplier_id, s.supplier_name, s.city, s.state
        ORDER BY total_revenue DESC
        """
        
        results4 = execute_query_and_display(cursor, query4,
            "Supplier Performance with Product Sales")
        
        if results4:
            column_names4 = [desc[0] for desc in cursor.description]
            export_to_csv(results4, column_names4, 'output_supplier_performance.csv')
        
        # Query 5: Monthly Sales Summary
        query5 = """
        SELECT 
            strftime('%Y-%m', o.order_date) AS month,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(DISTINCT o.customer_id) AS unique_customers,
            SUM(o.total_amount) AS total_revenue,
            AVG(o.total_amount) AS avg_order_value
        FROM orders o
        WHERE o.status != 'Cancelled'
        GROUP BY strftime('%Y-%m', o.order_date)
        ORDER BY month DESC
        """
        
        results5 = execute_query_and_display(cursor, query5,
            "Monthly Sales Summary")
        
        if results5:
            column_names5 = [desc[0] for desc in cursor.description]
            export_to_csv(results5, column_names5, 'output_monthly_sales.csv')
        
        print(f"\n{'='*80}")
        print("All queries completed successfully!")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"\nError executing queries: {str(e)}")
    finally:
        conn.close()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()

