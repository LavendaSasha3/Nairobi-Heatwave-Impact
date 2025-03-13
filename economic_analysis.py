
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr

# Data creation
df_health = pd.read_csv("C:/Users/FETO/Downloads/synthetic_nairobi_health_2023_2024.csv")
df_health["Date"] = pd.to_datetime(df_health["Date"])
df_econ = pd.DataFrame({
    "Date": df_health["Date"],
    "Economic Loss ($M)": (df_health["Nairobi Admissions"] * 500 / 1_000_000).round(2)
})
df_econ.to_csv("C:/Users/FETO/Downloads/nairobi_heatwave_economic_loss_2023_2024.csv", index=False)

# Analysis
total_loss = df_econ["Economic Loss ($M)"].sum()
print(f"Total Economic Loss (2023-2024): ${total_loss:.2f}M")
heatwave_months = df_health["Nairobi Admissions"] > 1000
avg_loss_heatwave = df_econ.loc[heatwave_months, "Economic Loss ($M)"].mean()
print(f"Average Loss During Heatwaves: ${avg_loss_heatwave:.2f}M")

# Plot
ds = xr.open_dataset("C:/Users/FETO/Downloads/era5_kenya_2023_2024.nc")
tasmax = ds["t2m"].resample(valid_time="1D").max() - 273.15
tasmax_nairobi = tasmax.sel(latitude=-1.29, longitude=36.82, method="nearest")
df_econ["Date"] = pd.to_datetime(df_econ["Date"])

fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(tasmax_nairobi.valid_time, tasmax_nairobi, label="Nairobi Max Temp", color="purple")
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature (°C)", color="purple")
ax1.tick_params(axis="y", labelcolor="purple")
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.plot(df_econ["Date"], df_econ["Economic Loss ($M)"], label="Economic Loss ($M)", color="orange")
ax2.set_ylabel("Economic Loss ($M)", color="orange")
ax2.tick_params(axis="y", labelcolor="orange")
ax2.legend(loc="upper right")

plt.title("Nairobi Heatwaves vs. Economic Losses (2023-2024)")
plt.grid()
plt.tight_layout()
plt.savefig("C:/Users/FETO/Downloads/heatwave_economic_loss.png", dpi=300)
plt.show()