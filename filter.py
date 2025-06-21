import pandas as pd

# 1. Load the full WHID dataset
original_file = "Web Hacking Incident Database (WHID) - Web Hacking Incident Database (WHID).csv"
df = pd.read_csv(original_file)

# 2. Display unique attack methods (for verification)
print("Unique attack methods in the dataset:")
print(df['Attack Method'].value_counts())

# 3. Filter only rows where Attack Method is 'SQL Injection'
df_sqli = df[df['Attack Method'] == 'SQL Injection']

# 4. Report number of SQLi incidents
print(f"\nNumber of SQL Injection incidents: {len(df_sqli)}")

# 5. Save the filtered data to a new file (do not overwrite original)
filtered_file = "whid_sql_injection_filtered.csv"
df_sqli.to_csv(filtered_file, index=False)
print(f"Filtered SQL Injection data saved to: {filtered_file}")
