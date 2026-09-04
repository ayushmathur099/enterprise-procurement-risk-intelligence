import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("enterprise_procurement.db")

query = """
SELECT
    s.Category,
    ROUND(
        AVG(
            julianday(po.Delivery_Date) -
            julianday(po.Order_Date)
        ),
        2
    ) AS Avg_Lead_Time
FROM Purchase_Orders po
JOIN Suppliers s
ON po.Supplier_ID = s.Supplier_ID
GROUP BY s.Category
ORDER BY Avg_Lead_Time DESC;
"""

df = pd.read_sql_query(query, conn)

print(df)

plt.figure(figsize=(10,6))
plt.bar(df["Category"], df["Avg_Lead_Time"])

plt.title("Average Lead Time by Supplier Category")
plt.xlabel("Supplier Category")
plt.ylabel("Average Lead Time (Days)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

conn.close()