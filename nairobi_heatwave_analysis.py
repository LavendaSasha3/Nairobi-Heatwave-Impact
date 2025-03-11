import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import numpy as np

# Load ERA5
ds = xr.open_dataset("C:/Users/FETO/Downloads/era5_kenya_2023_2024.nc")
tasmax = ds["t2m"].resample(valid_time="1D").max() - 273.15
tasmax_nairobi = tasmax.sel(latitude=-1.29, longitude=36.82, method="nearest")

# Detect Heatwaves (29°C tweak)
threshold = 29
runs = np.zeros(len(tasmax_nairobi), dtype=int)
run_id = 0
for i in range(1, len(tasmax_nairobi)):
    if tasmax_nairobi[i] > threshold and tasmax_nairobi[i-1] <= threshold:
        run_id += 1
    if tasmax_nairobi[i] > threshold:
        runs[i] = run_id
runs_xr = xr.DataArray(runs, dims="valid_time", coords={"valid_time": tasmax_nairobi.valid_time})
heatwave_count = (tasmax_nairobi > threshold).groupby(runs_xr).sum()
heatwaves = heatwave_count[heatwave_count >= 3]
heatwave_starts = tasmax_nairobi.valid_time.where((runs_xr > 0) & (runs_xr.diff("valid_time") > 0) & (heatwave_count[runs_xr-1] >= 3), drop=True).values

# Load Synthetic Data
df = pd.read_csv("C:/Users/FETO/Downloads/synthetic_nairobi_health_2023_2024.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Plot
fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(tasmax_nairobi.valid_time, tasmax_nairobi, label="Nairobi Max Temp", color="purple", linewidth=1.5)
for i in range(len(heatwaves)):
    ax1.axvspan(heatwave_starts[i], heatwave_starts[i] + np.timedelta64(int(heatwaves[i] - 1), "D"), color="red", alpha=0.3)
ax1.axhline(y=threshold, color="green", linestyle=":", label="Threshold (29°C)")
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature (°C)", color="purple")
ax1.tick_params(axis="y", labelcolor="purple")
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.plot(df["Date"], df["Nairobi Admissions"], label="Hospital Admissions", color="blue", linewidth=1.5)
ax2.set_ylabel("Admissions", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")
ax2.legend(loc="upper right")

plt.title("Nairobi Heatwaves vs. Admissions (2023-2024)", fontsize=14)
plt.grid()
plt.tight_layout()
plt.savefig("C:/Users/FETO/Downloads/heatwave_admissions.png", dpi=300)
plt.show()
