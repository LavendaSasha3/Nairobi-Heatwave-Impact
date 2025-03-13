import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create synthetic drought data
dates = pd.date_range(start="2023-01-01", end="2024-12-01", freq="MS")
df_drought = pd.DataFrame({
    "Date": dates,
    "Rainfall (mm)": np.random.uniform(20, 100, len(dates)),
    "Maize Yield (tonnes)": np.random.uniform(800, 1200, len(dates))
})

# Simulate drought impact
df_drought.loc[df_drought["Rainfall (mm)"] < 40, "Maize Yield (tonnes)"] *= 0.7
df_drought["Yield Loss (tonnes)"] = 1000 - df_drought["Maize Yield (tonnes)"]
df_drought["Economic Loss ($M)"] = (df_drought["Yield Loss (tonnes)"] * 200 / 1_000_000).round(2)
df_drought.to_csv("C:/Users/FETO/Downloads/kenya_drought_impact_2023_2024.csv", index=False)

# Calculate economic impact
total_loss = df_drought["Economic Loss ($M)"].sum()
print(f"Total Economic Loss from Droughts (2023-2024): ${total_loss:.2f}M")
drought_months = df_drought["Rainfall (mm)"] < 40
avg_loss_drought = df_drought.loc[drought_months, "Economic Loss ($M)"].mean()
print(f"Average Loss During Drought Months: ${avg_loss_drought:.2f}M")

# Visualize
fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(df_drought["Date"], df_drought["Rainfall (mm)"], label="Rainfall (mm)", color="blue")
ax1.set_xlabel("Time")
ax1.set_ylabel("Rainfall (mm)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.plot(df_drought["Date"], df_drought["Economic Loss ($M)"], label="Economic Loss ($M)", color="red")
ax2.set_ylabel("Economic Loss ($M)", color="red")
ax2.tick_params(axis="y", labelcolor="red")
ax2.legend(loc="upper right")

plt.title("Kenya Droughts vs. Economic Losses for Farmers (2023-2024)")
plt.grid()
plt.tight_layout()
plt.savefig("C:/Users/FETO/Downloads/drought_economic_loss.png", dpi=300)
plt.show()