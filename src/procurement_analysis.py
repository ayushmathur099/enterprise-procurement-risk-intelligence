import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("enterprise_procurement.db")

query = """
SELECT
    Supplier_ID,
    ROUND(SUM(Total_Cost), 2) AS Total_Spend
FROM Purchase_Orders
GROUP BY Supplier_ID
ORDER BY Total_Spend DESC
LIMIT 10;
"""

top_suppliers = pd.read_sql_query(query, conn)

print(top_suppliers)

plt.figure(figsize=(10, 6))
plt.bar(
    top_suppliers["Supplier_ID"].astype(str),
    top_suppliers["Total_Spend"]
)

plt.title("Top 10 Suppliers by Procurement Spend")
plt.xlabel("Supplier ID")
plt.ylabel("Total Spend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

conn.close()