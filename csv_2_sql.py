import sqlite3
import pandas as pd

# Load the cleaned CSV
df = pd.read_csv("/Users/hq/Downloads/gdp360v2/master_data.csv")

# Connect to SQLite DB (creates file if not exists)
conn = sqlite3.connect("master_gdp.db")

# Push DataFrame to SQLite
df.to_sql("gdp_data", conn, if_exists="replace", index=False)

conn.close()
print("✅ Data inserted into master_gdp.db")