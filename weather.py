
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Date": [
        "2026-09-01", "2026-09-02", "2026-09-03",
        "2026-09-04", "2026-09-05", "2026-09-06",
        "2026-09-07", "2026-09-08", "2026-09-09",
        "2026-09-10", "2026-09-11", "2026-09-12",
        "2026-09-13", "2026-09-14", "2026-09-15",
        "2026-09-01"
    ],
    "City": [
        " islamabad", "ISLAMABAD ", "Islamabad",
        " lahore", "LAHORE ", "Karachi",
        "KARACHI", " karachi ", "Islamabad",
        "Lahore", " lahore ", "KARACHI",
        "ISLAMABAD", "lahore", " Karachi",
        "ISLAMABAD"
    ],
    "Temperature": [
        "30C", "32C", "31C", "29C", "28C",
        "34C", "33C", "35C", "27C", "30C",
        "31C", "29C", "28C", "32C", "33C",
        "30C"
    ],
    "Humidity": [
        55, None, 60, 58, None, 65, 50, 62,
        None, 57, 59, 54, 61, 56, 58, 55
    ],
    "Condition": [
        " sunny", "CLOUDY ", "Sunny", " Rainy",
        "cloudy", "SUNNY", " Cloudy", "sunny ",
        "RAINY", "CLOUDY", " Sunny", "rainy ",
        "Cloudy", "SUNNY", "sunny", "SUNNY"
    ]
}

df = pd.DataFrame(data)

df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()

df["Temperature"] = (
    df["Temperature"]
    .str.replace("C", "", regex=False)
    .astype(float)
)

df["Date"] = pd.to_datetime(df["Date"])

df = df.drop_duplicates().copy()

print("Rows after dropping duplicates:", len(df))

df["Humidity"] = df["Humidity"].fillna(
    df["Humidity"].median()
)

print(
    "Missing Humidity filled with median:",
    df["Humidity"].median()
)

df_encoded = pd.get_dummies(
    df, columns=["Condition"], dtype=int
)

print("\nEncoded Condition Columns:")
print(df_encoded.filter(like="Condition_").head())

condition_counts = df["Condition"].value_counts()
print("\nCondition counts:")
print(condition_counts)

correlation = df["Temperature"].corr(df["Humidity"])
print(
    "\nCorrelation (Temperature, Humidity):",
    round(correlation, 3)
)

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(
    df["Date"], df["Temperature"], marker="o"
)
axes[0, 0].set_title("Temperature Over Time")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (C)")
axes[0, 0].tick_params(axis="x", rotation=45)

axes[0, 1].scatter(
    df["Temperature"], df["Humidity"]
)
axes[0, 1].set_title("Temperature vs Humidity")
axes[0, 1].set_xlabel("Temperature (C)")
axes[0, 1].set_ylabel("Humidity")

axes[1, 0].pie(
    condition_counts.values,
    labels=condition_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1, 0].set_title("Weather Condition Distribution")

axes[1, 1].hist(
    df["Temperature"], bins=5, edgecolor="black"
)
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (C)")
axes[1, 1].set_ylabel("Number of Days")

fig.suptitle("Weather Overview", fontsize=16)
fig.tight_layout()
plt.savefig("weather_dashboard.png")
plt.show()
