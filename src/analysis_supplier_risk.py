print("Program Started")
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("enterprise_procurement.db")

query = """
SELECT
    s.Supplier_ID,
    s.Supplier_Name,
    s.Category,
    s.Risk_Score,
    s.Performance_Score,
    c.Country_Name,
    c.Risk_Level,
    ROUND(SUM(po.Total_Cost), 2) AS Total_Spend
FROM Suppliers s
JOIN Countries c
    ON s.Country_ID = c.Country_ID
JOIN Purchase_Orders po
    ON s.Supplier_ID = po.Supplier_ID
GROUP BY
    s.Supplier_ID,
    s.Supplier_Name,
    s.Category,
    s.Risk_Score,
    s.Performance_Score,
    c.Country_Name,
    c.Risk_Level
ORDER BY
    s.Risk_Score DESC,
    s.Performance_Score ASC,
    Total_Spend DESC
LIMIT 15;
"""

df = pd.read_sql_query(query, conn)

print(df)

plt.figure(figsize=(12, 7))

plt.barh(
    df["Supplier_Name"],
    df["Risk_Score"]
)

plt.title("Top High-Risk Suppliers")
plt.xlabel("Supplier Risk Score")
plt.ylabel("Supplier")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

conn.close()