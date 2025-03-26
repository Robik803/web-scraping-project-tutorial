import bs4
import requests
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

#Download the HTML

url = "https://companies-market-cap-copy.vercel.app/index.html"

response = requests.get(url)

html_content = response.text

#Transform the DataFrame

soup = bs4.BeautifulSoup(html_content, "html.parser")

table = soup.find("table")

rows = table.find_all("tr")

data = []
for row in rows[1:]:
    cols = row.find_all("td")
    date = cols[0].text.strip()
    revenue = cols[1].text.strip()
    data.append([date, revenue])

    df = pd.DataFrame(data, columns=["Date", "Revenue"])

df = df.sort_values("Date")

#Process the DataFrame

def convert_revenue(value):
    if "B" in value:
        edit_value = float(value.replace("B", "").replace("$", "").replace(",", ""))
        return edit_value


df["Revenue"] = df["Revenue"].apply(convert_revenue)

#Store the data in SQLite

conn = sqlite3.connect("tesla_revenues.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS revenue (
    date TEXT,
    revenue REAL
)
""")

for index, row in df.iterrows():
    cursor.execute("INSERT INTO revenue (date, revenue) VALUES (?, ?)", (row["Date"], row["Revenue"]))

conn.commit()
conn.close()

#Visualize the data

    #Plot-Line Chart

plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Revenue"], marker='o', label="Revenue")
plt.title("Tesla annual revenue")
plt.xlabel("Date")
plt.ylabel("Revenue in billions (USD)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.savefig("revenue_plot.png")
plt.show()

    #Bar Chart

plt.figure(figsize=(10, 6))
plt.bar(df["Date"], df["Revenue"], label="Revenue")
plt.title("Tesla annual revenue")
plt.xlabel("Date")
plt.ylabel("Revenue in billions (USD)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.savefig("revenue_bars.png")
plt.show()

    #Pie Chart

plt.figure(figsize=(10, 6))
plt.pie(df['Revenue'], labels=df['Date'])
plt.title('Tesla Metrics - Pie Chart')
plt.axis('equal')
plt.savefig("revenue_pie.png")
plt.show()