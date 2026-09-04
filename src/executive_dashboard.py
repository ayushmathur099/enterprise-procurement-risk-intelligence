print("Program Started")

import sqlite3
import pandas as pd
import matplotlib

# Prevent GUI issues on macOS
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_ROOT / "enterprise_procurement.db"
REPORTS_PATH = PROJECT_ROOT / "reports"

REPORTS_PATH.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

print("Database Connected")


# ==========================================================
# KPI QUERIES
# ==========================================================

total_spend = pd.read_sql_query("""
SELECT
    SUM(Total_Cost) AS Total_Spend
FROM Purchase_Orders;
""", conn).iloc[0, 0]

total_suppliers = pd.read_sql_query("""
SELECT
    COUNT(*) AS Total_Suppliers
FROM Suppliers;
""", conn).iloc[0, 0]

total_orders = pd.read_sql_query("""
SELECT
    COUNT(*) AS Total_Orders
FROM Purchase_Orders;
""", conn).iloc[0, 0]

avg_performance = pd.read_sql_query("""
SELECT
    AVG(Performance_Score) AS Avg_Performance
FROM Suppliers;
""", conn).iloc[0, 0]

avg_risk = pd.read_sql_query("""
SELECT
    AVG(Risk_Score) AS Avg_Risk
FROM Suppliers;
""", conn).iloc[0, 0]

avg_lead_time = pd.read_sql_query("""
SELECT
    AVG(
        julianday(Delivery_Date) -
        julianday(Order_Date)
    ) AS Avg_Lead_Time
FROM Purchase_Orders;
""", conn).iloc[0, 0]


# ==========================================================
# TOP SUPPLIERS BY SPEND
# ==========================================================

top_suppliers = pd.read_sql_query("""
SELECT
    s.Supplier_Name,
    SUM(po.Total_Cost) AS Total_Spend
FROM Purchase_Orders po
JOIN Suppliers s
    ON po.Supplier_ID = s.Supplier_ID
GROUP BY
    s.Supplier_ID,
    s.Supplier_Name
ORDER BY Total_Spend DESC
LIMIT 10;
""", conn)


# ==========================================================
# PROCUREMENT SPEND BY CATEGORY
# ==========================================================

category_spend = pd.read_sql_query("""
SELECT
    p.Category,
    SUM(po.Total_Cost) AS Total_Spend
FROM Purchase_Orders po
JOIN Products p
    ON po.Product_ID = p.Product_ID
GROUP BY p.Category
ORDER BY Total_Spend DESC;
""", conn)


# ==========================================================
# COUNTRY PROCUREMENT EXPOSURE
# ==========================================================

country_spend = pd.read_sql_query("""
SELECT
    c.Country_Name,
    SUM(po.Total_Cost) AS Total_Spend
FROM Purchase_Orders po
JOIN Suppliers s
    ON po.Supplier_ID = s.Supplier_ID
JOIN Countries c
    ON s.Country_ID = c.Country_ID
GROUP BY c.Country_Name
ORDER BY Total_Spend DESC;
""", conn)


# ==========================================================
# PURCHASE ORDER STATUS
# ==========================================================

order_status = pd.read_sql_query("""
SELECT
    Order_Status,
    COUNT(*) AS Orders
FROM Purchase_Orders
GROUP BY Order_Status;
""", conn)


# ==========================================================
# CREATE DASHBOARD
# ==========================================================

fig = plt.figure(figsize=(18, 14))

fig.suptitle(
    "Enterprise Procurement Risk Intelligence Dashboard",
    fontsize=22,
    fontweight="bold"
)


# ==========================================================
# KPI CARDS
# ==========================================================

kpis = [
    ("Total Procurement Spend", f"${total_spend / 1_000_000_000:.2f}B"),
    ("Total Suppliers", f"{total_suppliers:,}"),
    ("Purchase Orders", f"{total_orders:,}"),
    ("Avg Supplier Performance", f"{avg_performance:.1f}"),
    ("Avg Supplier Risk", f"{avg_risk:.2f} / 10"),
    ("Avg Lead Time", f"{avg_lead_time:.1f} Days")
]

for i, (title, value) in enumerate(kpis):

    ax = fig.add_subplot(4, 3, i + 1)

    ax.axis("off")

    ax.text(
        0.5,
        0.62,
        value,
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold"
    )

    ax.text(
        0.5,
        0.30,
        title,
        ha="center",
        va="center",
        fontsize=11
    )

    ax.set_title("")


# ==========================================================
# TOP SUPPLIERS
# ==========================================================

ax1 = fig.add_subplot(4, 2, 5)

supplier_plot = top_suppliers.sort_values(
    "Total_Spend",
    ascending=True
)

ax1.barh(
    supplier_plot["Supplier_Name"],
    supplier_plot["Total_Spend"] / 1_000_000
)

ax1.set_title("Top 10 Suppliers by Procurement Spend")

ax1.set_xlabel("Spend ($ Millions)")

ax1.set_ylabel("")


# ==========================================================
# CATEGORY SPEND
# ==========================================================

ax2 = fig.add_subplot(4, 2, 6)

ax2.bar(
    category_spend["Category"],
    category_spend["Total_Spend"] / 1_000_000
)

ax2.set_title("Procurement Spend by Category")

ax2.set_ylabel("Spend ($ Millions)")

ax2.tick_params(
    axis="x",
    rotation=45
)


# ==========================================================
# COUNTRY EXPOSURE
# ==========================================================

ax3 = fig.add_subplot(4, 2, 7)

country_plot = country_spend.sort_values(
    "Total_Spend",
    ascending=True
)

ax3.barh(
    country_plot["Country_Name"],
    country_plot["Total_Spend"] / 1_000_000
)

ax3.set_title("Procurement Exposure by Country")

ax3.set_xlabel("Spend ($ Millions)")

ax3.set_ylabel("")


# ==========================================================
# ORDER STATUS
# ==========================================================

ax4 = fig.add_subplot(4, 2, 8)

ax4.pie(
    order_status["Orders"],
    labels=order_status["Order_Status"],
    autopct="%1.1f%%",
    startangle=90
)

ax4.set_title("Purchase Order Status Distribution")

# ==========================================================
# DASHBOARD SPACING
# ==========================================================

plt.subplots_adjust(
    hspace=0.65,
    wspace=0.35,
    top=0.93
)

# ==========================================================
# SAVE DASHBOARD
# ==========================================================

output_file = REPORTS_PATH / "executive_procurement_dashboard.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()

conn.close()

print("Executive Dashboard Created Successfully")
print("Saved to:", output_file)