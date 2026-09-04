import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("enterprise_procurement.db")

query = """
SELECT
Order_Status,
COUNT(*) AS Orders
FROM Purchase_Orders
GROUP BY Order_Status;
"""

df = pd.read_sql_query(query, conn)

print(df)

plt.figure(figsize=(6,6))
plt.pie(
    df["Orders"],
    labels=df["Order_Status"],
    autopct="%1.1f%%"
)

plt.title("Purchase Order Status")
plt.show()

conn.close()