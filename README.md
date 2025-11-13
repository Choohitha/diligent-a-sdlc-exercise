# Ecommerce Data Pipeline Project - Diligent A-SDLC Exercise

This project demonstrates the use of Cursor IDE to create prompts for an ecommerce data pipeline, following the A-SDLC (AI-Software Development Life Cycle) approach.

## 🎯 Main Deliverables - Prompts

This assignment focuses on creating **three prompts** that can be used in Cursor IDE to generate code for:

1. **`prompt_generate_data.txt`** - Prompt to generate synthetic ecommerce data (5 CSV files)
2. **`prompt_ingest_database.txt`** - Prompt to ingest CSV data into SQLite database
3. **`prompt_sql_query.txt`** - Prompt to generate SQL queries with multiple table joins

These prompts can be used directly in Cursor IDE to generate the complete data pipeline solution.

> **Note:** The Python scripts, data files, and database included in this repository serve as **proof of concept** - demonstrating that the prompts successfully generate working code when used in Cursor IDE.

## 📋 Project Structure
```
Diligent/
├── data/                          # Generated CSV data files
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── suppliers.csv
├── ecommerce.db                   # SQLite database (generated)
├── generate_data.py               # Script to generate synthetic data
├── ingest_data.py                 # Script to ingest data into SQLite
├── query_data.py                  # Script to execute SQL queries
├── prompt_generate_data.txt       # Prompt for data generation
├── prompt_ingest_database.txt     # Prompt for database ingestion
├── prompt_sql_query.txt           # Prompt for SQL queries
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```
The following scripts were generated using the prompts above in Cursor IDE:

### Setup Instructions
1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Synthetic Data**
   ```bash
   python generate_data.py
   ```
   This will create 5 CSV files in the `data/` directory:
   - `customers.csv` (100 customers)
   - `products.csv` (80 products)
   - `orders.csv` (150 orders)
   - `order_items.csv` (order line items)
   - `suppliers.csv` (15 suppliers)

3. **Ingest Data into SQLite Database**
   ```bash
   python ingest_data.py
   ```
   This will create `ecommerce.db` and populate it with data from the CSV files.

4. **Execute SQL Queries**
   ```bash
   python query_data.py
   ```
   This will execute multiple complex SQL queries with joins and export results to CSV files.

## 📝 Prompt Details

### 1. Generate Synthetic Ecommerce Data
**File:** `prompt_generate_data.txt`

This prompt instructs Cursor IDE to create a Python script that generates 5 CSV files with realistic ecommerce data:
- `customers.csv` - Customer information
- `products.csv` - Product catalog  
- `orders.csv` - Order records
- `order_items.csv` - Individual items in each order
- `suppliers.csv` - Supplier information

### 2. Ingest Data into SQLite Database
**File:** `prompt_ingest_database.txt`

This prompt instructs Cursor IDE to create a Python script that:
- Creates a SQLite database (`ecommerce.db`)
- Defines proper schema with foreign key relationships
- Loads all CSV files into corresponding tables
- Handles data type conversions and errors

### 3. Generate SQL Queries with Joins
**File:** `prompt_sql_query.txt`

This prompt instructs Cursor IDE to create a Python script that:
- Connects to the SQLite database
- Executes complex SQL queries joining 3-4 tables
- Displays results in readable format
- Exports results to CSV files

## 💻 Implementation (Generated from Prompts)

## Database Schema

The SQLite database contains the following tables:

- **customers**: Customer information
- **products**: Product catalog
- **orders**: Order records
- **order_items**: Individual items in each order
- **suppliers**: Supplier information

All tables have appropriate foreign key relationships to maintain referential integrity.

## SQL Queries

The `query_data.py` script executes 5 different queries:

1. **Detailed Order History**: Joins customers, orders, order_items, and products
2. **Sales by Category**: Aggregates sales data by product category
3. **Top Customers**: Identifies top customers by total spending
4. **Supplier Performance**: Analyzes supplier performance with product sales
5. **Monthly Sales Summary**: Provides monthly sales statistics

All query results are exported to CSV files in the project root.

## 🔗 GitHub Repository

This project has been pushed to GitHub:
**Repository:** https://github.com/Choohitha/diligent-a-sdlc-exercise.git

## 📌 Notes
- All scripts include error handling and progress messages
- The data generation uses the Faker library for realistic synthetic data
- Foreign key constraints ensure data integrity
- CSV exports are UTF-8 encoded for international character support