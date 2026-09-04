import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("enterprise_procurement.db")

query = """
SELECT
    c.Country_Name,
    c.Risk_Level,
    ROUND(SUM(po.Total_Cost),2) AS Total_Spend
FROM Purchase_Orders po
JOIN Suppliers s
    ON po.Supplier_ID = s.Supplier_ID
JOIN Countries c
    ON s.Country_ID = c.Country_ID
GROUP BY
    c.Country_Name,
    c.Risk_Level
ORDER BY
    Total_Spend DESC;
"""

df = pd.read_sql_query(query, conn)

print(df)

plt.figure(figsize=(11,6))
plt.bar(df["Country_Name"], df["Total_Spend"])

plt.title("Procurement Spend by Country")
plt.xlabel("Country")
plt.ylabel("Total Procurement Spend")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(
    "reports/country_risk_dashboard.png",
    bbox_inches="tight"
)

print("Country risk chart saved successfully.")

conn.close()