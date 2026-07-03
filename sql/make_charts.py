import pandas as pd
import matplotlib.pyplot as plt
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
CHART_DIR = os.path.join(OUT_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")

# 1. Trip volume by hour
df = pd.read_csv(os.path.join(OUT_DIR, "trip_volume_by_hour.csv"))
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(df["pickup_hour"], df["trip_count"], color="#f1c40f", edgecolor="#333")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Trip Count")
ax.set_title("Trip Volume by Hour of Day")
ax.set_xticks(range(0, 24, 2))
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "trip_volume_by_hour.png"), dpi=150)
plt.close()

# 2. Trip volume by day of week
df = pd.read_csv(os.path.join(OUT_DIR, "trip_volume_by_dow.csv"))
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(df["day_name"], df["trip_count"], color="#2980b9")
ax.set_xlabel("Day of Week")
ax.set_ylabel("Trip Count")
ax.set_title("Trip Volume by Day of Week")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "trip_volume_by_dow.png"), dpi=150)
plt.close()

# 3. Tip percentage by payment type
df = pd.read_csv(os.path.join(OUT_DIR, "fare_tip_by_payment_type.csv"))
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(df["payment_type"], df["avg_tip_pct"], color="#27ae60")
ax.set_xlabel("Payment Type")
ax.set_ylabel("Average Tip (% of fare)")
ax.set_title("Average Tip % by Payment Type")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "tip_pct_by_payment_type.png"), dpi=150)
plt.close()

# 4. Average speed by hour
df = pd.read_csv(os.path.join(OUT_DIR, "speed_by_hour.csv"))
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df["pickup_hour"], df["avg_speed_mph"], linewidth=2, color="#c0392b", marker="o", markersize=4)
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Average Speed (mph)")
ax.set_title("Average Trip Speed by Hour of Day")
ax.set_xticks(range(0, 24, 2))
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "speed_by_hour.png"), dpi=150)
plt.close()

# 5. Distance distribution
df = pd.read_csv(os.path.join(OUT_DIR, "distance_distribution.csv"))
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(df["distance_band"], df["trip_count"], color="#8e44ad")
ax.set_xlabel("Trip Distance Band")
ax.set_ylabel("Trip Count")
ax.set_title("Trip Distance Distribution")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "distance_distribution.png"), dpi=150)
plt.close()

print(f"5 charts saved to {CHART_DIR}")
