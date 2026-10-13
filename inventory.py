
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Product": ["Cola", "Chips", "Milk", "Biscuits", "Juice",
                "Cheese", "Soda", "Cookies", "Yogurt", "Water"],
    "Category": ["beverages ", "SNACKS", " Dairy", "Snacks",
                 "beverages", "DAIRY ", "Beverages", " snacks ",
                 "dairy", "BEVERAGES"],
    "Price": ["Rs. 1,250", "Rs. 90", "Rs. 450", "Rs. 120",
              "Rs. 1,800", "Rs. 650", "Rs. 800", "Rs. 150",
              "Rs. 300", "Rs. 100"],
    "Stock": [40, 120, 60, 100, 50, 30, 70, 80, 45, 150]
}

df = pd.DataFrame(data)

df["Category"] = df["Category"].str.strip().str.title()

df["Price"] = (
    df["Price"]
    .str.replace("Rs. ", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

df["Category_Code"] = df["Category"].astype("category").cat.codes

print("Cleaned Inventory Data:")
print(df)

avg_price = df.groupby("Category")["Price"].mean()
stock_share = df.groupby("Category")["Stock"].sum()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(avg_price.index, avg_price.values)
axes[0].set_title("Average Price by Category")
axes[0].set_xlabel("Category")
axes[0].set_ylabel("Average Price (Rs.)")

axes[1].pie(
    stock_share.values,
    labels=stock_share.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1].set_title("Stock Share by Category")

fig.tight_layout()
plt.savefig("inventory_plots.png")
plt.show()
