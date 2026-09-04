import sqlite3
import pandas as pd

# Create database
conn = sqlite3.connect("enterprise_procurement.db")

# Load CSV files
countries = pd.read_csv("data/raw/countries.csv")
suppliers = pd.read_csv("data/raw/suppliers.csv")
products = pd.read_csv("data/raw/products.csv")
purchase_orders = pd.read_csv("data/raw/purchase_orders.csv")

# Write tables
countries.to_sql("Countries", conn, if_exists="replace", index=False)
suppliers.to_sql("Suppliers", conn, if_exists="replace", index=False)
products.to_sql("Products", conn, if_exists="replace", index=False)
purchase_orders.to_sql("Purchase_Orders", conn, if_exists="replace", index=False)

print("Database Created Successfully!")

conn.close()