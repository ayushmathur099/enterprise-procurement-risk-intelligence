import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("enterprise_procurement.db")

query = """
SELECT
    p.Category,
    ROUND(SUM(po.Total_Cost),2) AS Total_Spend
FROM Purchase_Orders po
JOIN Products p
ON po.Product_ID = p.Product_ID
GROUP BY p.Category
ORDER BY Total_Spend DESC;
"""

df = pd.read_sql_query(query, conn)

print(df)

plt.figure(figsize=(10,6))
plt.bar(df["Category"], df["Total_Spend"])

plt.title("Procurement Spend by Product Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

conn.close()