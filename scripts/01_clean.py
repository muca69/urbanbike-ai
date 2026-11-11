
import numpy as np
import pandas as pd
from config.common import DATA, SEED, save_json

# 1. Leximi i te dhenave
uci = pd.read_csv(DATA / "raw" / "day.csv")

columns = [
    "dteday", "cnt", "weekday",
    "mnth", "workingday", "holiday"
]

bikes = uci[columns].rename(columns={
    "dteday": "date",
    "cnt": "rentals",
    "mnth": "month"
})

weather = pd.read_csv(DATA / "raw" / "nasa_weather.csv")

# 2. Bashkimi i dy dataseteve
source = bikes.merge(weather, on="date", validate="one_to_one")
source = source.sort_values("date").reset_index(drop=True)

assert len(source) == 731
assert source["date"].is_unique

source.to_csv(DATA / "processed" / "merged_original.csv", index=False)

# 3. Krijimi i nje kopjeje me probleme per mesim
dirty = source.copy().astype(object)
order = np.random.default_rng(SEED).permutation(len(dirty))

dirty.loc[order[:18], "temp_c"] = np.nan
dirty.loc[order[18:30], "rain_mm"] = np.nan
dirty.loc[order[30:36], "temp_c"] = "gabim"

dirty = pd.concat(
    [dirty, dirty.iloc[order[52:64]]],
    ignore_index=True
)

dirty = dirty.sample(frac=1, random_state=SEED)
dirty.to_csv(DATA / "teaching" / "dirty.csv", index=False)

save_json("teaching_changes.json", {
    "purpose": "Probleme te injektuara vetem per mesim",
    "seed": SEED,
    "missing_temp": 18,
    "missing_rain": 12,
    "invalid_temp_text": 6,
    "duplicated_rows": 12
})

# 4. Auditimi i cilesise
data = pd.read_csv(DATA / "teaching" / "dirty.csv")

audit = {
    "uci_original_rows": len(uci),
    "uci_original_missing_cells": int(uci.isna().sum().sum()),
    "nasa_rows": len(weather),
    "joined_rows": len(source),
    "teaching_rows_before": len(data),
    "exact_duplicates_before": int(data.duplicated().sum()),
    "blank_cells_before": int(data.isna().sum().sum()),
    "dtypes_before": data.dtypes.astype(str).to_dict()
}

# 5. Pastrimi
clean = data.drop_duplicates().copy()
clean["date"] = pd.to_datetime(clean["date"], errors="raise")

for column in clean.columns.drop("date"):
    clean[column] = pd.to_numeric(clean[column], errors="coerce")

clean = clean.sort_values("date").reset_index(drop=True)

assert clean["date"].is_unique
assert clean["rentals"].notna().all()
assert clean["date"].diff().dropna().eq(pd.Timedelta(days=1)).all()

# 6. Feature Engineering
for lag in [1, 7]:
    clean[f"rentals_lag{lag}"] = clean["rentals"].shift(lag)

clean["rentals_mean7"] = (
    clean["rentals"].shift(1).rolling(7).mean()
)

for column in ["temp_c", "rain_mm", "wind_ms"]:
    clean[f"{column}_lag7"] = clean[column].shift(7)

clean["trend_days"] = (
    clean["date"] - clean["date"].min()
).dt.days

model_data = clean.iloc[7:].copy()

# 7. Ruajtja e rezultateve
clean.to_csv(DATA / "processed" / "cleaned_daily.csv", index=False)
model_data.to_csv(DATA / "processed" / "model_data.csv", index=False)

audit.update({
    "clean_rows": len(clean),
    "model_rows": len(model_data),
    "dtypes_after": clean.dtypes.astype(str).to_dict(),
    "remaining_missing_weather": int(
        clean[["temp_c", "rain_mm", "wind_ms"]]
        .isna().sum().sum()
    ),
    "note": "Imputimi kryhet me vone brenda Pipeline, vetem nga train."
})

save_json("data_quality.json", audit)

print("UrbanBike AI - Data Preprocessing completed!")
print(audit)
