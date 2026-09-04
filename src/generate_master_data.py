import pandas as pd
from pathlib import Path

# Create output folder
output_path = Path("data/raw")
output_path.mkdir(parents=True, exist_ok=True)

# Country Master Table
countries = [
    [1, "United States", "North America", "Low"],
    [2, "Canada", "North America", "Low"],
    [3, "Germany", "Europe", "Low"],
    [4, "United Kingdom", "Europe", "Low"],
    [5, "France", "Europe", "Low"],
    [6, "India", "Asia", "Medium"],
    [7, "China", "Asia", "Medium"],
    [8, "Japan", "Asia", "Low"],
    [9, "Brazil", "South America", "Medium"],
    [10, "Mexico", "North America", "Medium"]
]

countries_df = pd.DataFrame(
    countries,
    columns=[
        "Country_ID",
        "Country_Name",
        "Region",
        "Risk_Level"
    ]
)

countries_df.to_csv(
    output_path / "countries.csv",
    index=False
)

print("="*50)
print("COUNTRY MASTER TABLE CREATED")
print("="*50)
print(countries_df)
print("="*50)
print("Saved Successfully!")

from faker import Faker
import random

fake = Faker()

supplier_categories = [
    "Electronics",
    "Packaging",
    "Raw Materials",
    "IT Services",
    "Logistics",
    "Office Supplies",
    "Manufacturing",
    "Marketing",
    "Professional Services",
    "Facilities"
]

payment_terms = [
    "Net 30",
    "Net 45",
    "Net 60",
    "Advance",
    "Immediate"
]

suppliers = []

for supplier_id in range(1001, 2001):

    suppliers.append({

        "Supplier_ID": supplier_id,

        "Supplier_Name": fake.company(),

        "Country_ID": random.randint(1,10),

        "Category": random.choice(supplier_categories),

        "Payment_Terms": random.choice(payment_terms),

        "Lead_Time_Days": random.randint(5,45),

        "Performance_Score": round(random.uniform(70,100),2),

        "Risk_Score": random.randint(1,10),

        "Annual_Contract_Value": random.randint(50000,3000000)

    })

suppliers_df = pd.DataFrame(suppliers)

suppliers_df.to_csv(
    output_path / "suppliers.csv",
    index=False
)

print("\nSupplier Master Table Created Successfully")
print(suppliers_df.head())

# -----------------------------
# PRODUCT MASTER
# -----------------------------

product_categories = [
    "Laptop",
    "Server",
    "Networking",
    "Office Equipment",
    "Packaging",
    "Raw Material",
    "Industrial Parts",
    "Furniture",
    "Electronics",
    "Software License"
]

products = []

for product_id in range(5001,7001):

    products.append({

        "Product_ID": product_id,

        "Supplier_ID": random.randint(1001,2000),

        "Product_Name": fake.word().title() + " Product",

        "Category": random.choice(product_categories),

        "Unit_Cost": round(random.uniform(20,5000),2),

        "MOQ": random.randint(10,500),

        "Annual_Demand": random.randint(100,15000)

    })

products_df = pd.DataFrame(products)

products_df.to_csv(
    output_path / "products.csv",
    index=False
)

print("\nProducts Created Successfully")
print(products_df.head())

# ==========================================
# PURCHASE ORDERS
# ==========================================

from datetime import timedelta

purchase_orders = []

statuses = [
    "Completed",
    "Pending",
    "Cancelled",
    "Delayed"
]

for po_id in range(100000, 150000):

    supplier_id = random.randint(1001, 2000)

    product_id = random.randint(5001, 7000)

    quantity = random.randint(20, 800)

    unit_cost = round(random.uniform(20, 5000), 2)

    order_date = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    delivery_date = order_date + timedelta(
        days=random.randint(5, 45)
    )

    purchase_orders.append({

        "PO_ID": po_id,

        "Supplier_ID": supplier_id,

        "Product_ID": product_id,

        "Order_Date": order_date,

        "Delivery_Date": delivery_date,

        "Quantity": quantity,

        "Unit_Cost": unit_cost,

        "Total_Cost": round(quantity * unit_cost, 2),

        "Order_Status": random.choice(statuses)

    })

po_df = pd.DataFrame(purchase_orders)

po_df.to_csv(
    output_path / "purchase_orders.csv",
    index=False
)

print("\nPurchase Orders Created Successfully")

print(po_df.head())