# ============================================================
# PROJE 2: HAVA DURUMU VERİ ANALİZİ (Munich Dataset)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")

# ------------------------------------------------------------
# KLASÖRLERİ OLUŞTUR
# ------------------------------------------------------------

os.makedirs("output", exist_ok=True)   # görseller buraya
os.makedirs("Report", exist_ok=True)   # rapor buraya


# ------------------------------------------------------------
# AŞAMA 1: VERİ YÜKLEME ve HAZIRLIK
# ------------------------------------------------------------

df = pd.read_csv("buraya dosya yolu girilecek")     # CSV ile .py aynı klasörde olmalı

if df.shape[1] == 1:
    df = df.iloc[:, 0].str.split(";", expand=True)
    df.columns = ["date", "precip_mm", "snow_cm"]

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["precip_mm"] = pd.to_numeric(df["precip_mm"], errors="coerce")
df["snow_cm"] = pd.to_numeric(df["snow_cm"], errors="coerce")

df = df.set_index("date")
df = df.fillna(0)


# ------------------------------------------------------------
# AŞAMA 2: EDA ANALİZİ
# ------------------------------------------------------------

total_precip = df["precip_mm"].sum()
total_snow = df["snow_cm"].sum()

max_rain_day = df["precip_mm"].idxmax()
max_rain = df["precip_mm"].max()

max_snow_day = df["snow_cm"].idxmax()
max_snow = df["snow_cm"].max()


# ------------------------------------------------------------
# AŞAMA 3: GÖRSELLEŞTİRME (GRAFİKLER output/ İÇİNE KAYDOLUR)
# ------------------------------------------------------------

# 1) Günlük Yağış
plt.figure(figsize=(12,4))
plt.plot(df.index, df["precip_mm"])
plt.title("Daily Precipitation in Munich")
plt.xlabel("Date")
plt.ylabel("Precipitation (mm)")
plt.grid(True)
plt.tight_layout()
plt.savefig("output/daily_precipitation.png")
plt.close()

# 2) Günlük Kar
plt.figure(figsize=(12,4))
plt.plot(df.index, df["snow_cm"])
plt.title("Daily Snowfall in Munich")
plt.xlabel("Date")
plt.ylabel("Snowfall (cm)")
plt.grid(True)
plt.tight_layout()
plt.savefig("output/daily_snowfall.png")
plt.close()

# 3) Aylık Ortalama Yağış
monthly_precip = df["precip_mm"].resample("M").mean()

plt.figure(figsize=(10,4))
plt.bar(monthly_precip.index, monthly_precip.values)
plt.title("Monthly Average Precipitation")
plt.xlabel("Month")
plt.ylabel("Avg Precip (mm)")
plt.tight_layout()
plt.savefig("output/monthly_avg_precip.png")
plt.close()

# 4) Aykırı Değerler
vals = df["precip_mm"].values.astype(float)
mean = np.mean(vals)
std = np.std(vals)

z = np.zeros_like(vals) if std == 0 else (vals - mean) / std
df["precip_z"] = z
outliers = df[np.abs(df["precip_z"]) > 3]

plt.figure(figsize=(12,4))
plt.plot(df.index, df["precip_mm"], label="Precipitation")
plt.scatter(outliers.index, outliers["precip_mm"], color="red", label="Outliers")
plt.title("Precipitation Outliers (Z > 3)")
plt.xlabel("Date")
plt.ylabel("mm")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("output/precip_outliers.png")
plt.close()


# ------------------------------------------------------------
# AŞAMA 4: RAPORLAMA (Report/rapor.txt)
# ------------------------------------------------------------

rapor_yolu = "Report/rapor.txt"

with open(rapor_yolu, "w", encoding="utf-8") as f:
    f.write("=== MUNICH WEATHER ANALYSIS REPORT ===\n\n")
    f.write(f"Toplam veri noktası: {df.shape[0]}\n\n")
    f.write(f"Toplam yağış: {total_precip:.2f} mm\n")
    f.write(f"En yağışlı gün: {max_rain_day.date()} — {max_rain} mm\n\n")
    f.write(f"Toplam kar: {total_snow:.2f} cm\n")
    f.write(f"En karlı gün: {max_snow_day.date()} — {max_snow} cm\n\n")
    f.write(f"Aykırı yağış sayısı: {len(outliers)}\n\n")
    f.write("Grafikler output klasörüne kaydedildi.\n")
    f.write("Rapor başarıyla oluşturuldu.\n")

print("\nRapor oluşturuldu → Report/rapor.txt")
print("Görseller kaydedildi → output/ klasörü\n")

