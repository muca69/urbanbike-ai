from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Vendndodhjet
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed" / "cleaned_daily.csv"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

# Leximi i datasetit të përdorur nga modeli ML
df = pd.read_csv(
    ROOT / "data/processed/model_data.csv",
    parse_dates=["date"]
)

df = df.sort_values("date").reset_index(drop=True)

# E njëjta periudhë train si modeli i grupit
train = df.loc[df["date"] <= "2012-04-30"].copy()

assert len(train) == 479

print("Periudha:", train["date"].min(), train["date"].max())
print("Korrelacioni:", train["temp_c"].corr(train["rentals"]))

# Statistikat
print("\n===== URBANBIKE AI - EDA =====")
print("Numri i ditëve:", len(train))
print("Mesatarja e qirave:", round(train["rentals"].mean(), 2))
print("Minimumi:", train["rentals"].min())
print("Maksimumi:", train["rentals"].max())
print("Devijimi standard:", round(train["rentals"].std(), 2))
print("Vlera që mungojnë:", train.isna().sum().sum())
print("Data të dyfishuara:", train["date"].duplicated().sum())

# Grafiku 1: Kërkesa ditore
plt.figure(figsize=(12, 5))
plt.plot(train["date"], train["rentals"])
plt.title("Daily Bike Rental Demand")
plt.xlabel("Date")
plt.ylabel("Number of Rentals")
plt.tight_layout()
plt.savefig(REPORTS / "01_daily_demand.png", dpi=150)
plt.close()

# Grafiku 2: Kërkesa mesatare mujore
monthly = train.groupby("month")["rentals"].mean()

plt.figure(figsize=(10, 5))
sns.barplot(x=monthly.index, y=monthly.values)
plt.title("Average Bike Rentals by Month")
plt.xlabel("Month")
plt.ylabel("Average Daily Rentals")
plt.tight_layout()
plt.savefig(REPORTS / "02_monthly_demand.png", dpi=150)
plt.close()

# Grafiku 3: Temperatura kundrejt kërkesës
plt.figure(figsize=(10, 5))
sns.scatterplot(data=train, x="temp_c", y="rentals", alpha=0.6)
plt.title("Temperature vs Bike Rental Demand")
plt.xlabel("Temperature (°C)")
plt.ylabel("Number of Rentals")
plt.tight_layout()
plt.savefig(REPORTS / "03_temperature_demand.png", dpi=150)
plt.close()

print("\nSUCCESS! 3 grafikët u krijuan.")
print("Grafikët janë ruajtur në:", REPORTS)