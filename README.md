# Ecommerce Data Pipeline Project

This project demonstrates a complete data pipeline for ecommerce data using Cursor IDE, following the A-SDLC (AI-Software Development Life Cycle) approach.

## Project Structure

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

## Setup Instructions

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

## Prompts Used

The project includes three main prompts that were used to generate the code:

1. **prompt_generate_data.txt**: Prompt for generating synthetic ecommerce data
2. **prompt_ingest_database.txt**: Prompt for ingesting data into SQLite database
3. **prompt_sql_query.txt**: Prompt for creating SQL queries with multiple table joins

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

## GitHub Repository

This project is configured for GitHub. To push to GitHub:

1. Create a repository on GitHub
2. Add the remote:
   ```bash
   git remote add origin <your-github-repo-url>
   ```
3. Commit and push:
   ```bash
   git add .
   git commit -m "Initial commit: Ecommerce data pipeline"
   git push -u origin main
   ```

## Notes

- All scripts include error handling and progress messages
- The data generation uses the Faker library for realistic synthetic data
- Foreign key constraints ensure data integrity
- CSV exports are UTF-8 encoded for international character support

