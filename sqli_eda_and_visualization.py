import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

# Load dataset
df = pd.read_csv("whid_sql_injection_filtered.csv")

# Convert date and extract year
df['Date Occurred'] = pd.to_datetime(df['Date Occurred'], errors='coerce')
df['Year'] = df['Date Occurred'].dt.year

# -------------------------------
# 1️⃣ ARO Trend by Year (Line Plot)
# -------------------------------
yearly_counts = df['Year'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.plot(yearly_counts.index, yearly_counts.values, marker='o', linestyle='-', color='blue')
plt.title('Annual SQL Injection Incidents (ARO Trend)')
plt.xlabel('Year')
plt.ylabel('Number of Incidents')
plt.xticks(ticks=range(int(yearly_counts.index.min()), int(yearly_counts.index.max()) + 1), rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("aro_trend_sql_injection_fixed.png")
plt.show()

# -------------------------------
# 2️⃣ Top 10 Application Weaknesses
# -------------------------------
top_weaknesses = df['Application Weakness'].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_weaknesses.plot(kind='bar', color='orange')
plt.title('Top 10 Application Weaknesses (SQL Injection Cases)')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("top_weaknesses_sql_injection.png")
plt.show()

# -------------------------------
# 3️⃣ Top 10 Keywords in Descriptions
# -------------------------------
text = " ".join(df['Incident Description'].dropna().astype(str)).lower()
words = re.findall(r'\b[a-z]{4,}\b', text)

#  stopwords set
stopwords = set([
    "attack", "site", "data", "user", "admin", "from", "this", "that", "with",
    "have", "been", "they", "their", "which", "when", "your", "some", "into",
    "after", "using", "more", "such", "were", "about", "also", "will", "them",
    "http", "https", "href", "html", "www", "com", "page", "read", "click",
    "index", "file", "script", "title", "php", "org", "net", "info",
    "include","company", "website", "information", "access", "news",
    "account", "system", "user", "customer", "organization"
])
filtered_words = [w for w in words if w not in stopwords]

# Count and plot
top_keywords = Counter(filtered_words).most_common(10)
keywords_df = pd.DataFrame(top_keywords, columns=["Keyword", "Count"])

plt.figure(figsize=(10, 6))
plt.bar(keywords_df["Keyword"], keywords_df["Count"], color='green')
plt.title("Top 10 Keywords in SQLi Descriptions")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_keywords_sqli_cleaned.png")
plt.show()
