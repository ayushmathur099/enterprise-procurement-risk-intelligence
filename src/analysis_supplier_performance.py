import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("enterprise_procurement.db")

query = """
SELECT
    Supplier_Name,
    Performance_Score
FROM Suppliers
ORDER BY Performance_Score DESC
LIMIT 10;
"""

df = pd.read_sql_query(query, conn)

print(df)

plt.figure(figsize=(11,6))
plt.barh(df["Supplier_Name"], df["Performance_Score"])

plt.title("Top Supplier Performance Scores")
plt.xlabel("Performance Score")
plt.tight_layout()
plt.show()

conn.close()