import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

colors = plt.cm.get_cmap('tab10').colors

# Read the CSV data into a DataFrame
data = pd.read_csv("./Collected Data/Collected Updated Labeled Data - Phase 01/participant 19.csv")

stairs_data = data[pd.to_numeric(data["Timestamp"]) >= 798 ]


stairs_data_temp = stairs_data[pd.to_numeric(stairs_data["Timestamp"]) < 823]


stairs_data_t = stairs_data_temp[stairs_data_temp["Label"] == "Lift down"]

# Select the columns you want to plot (assuming x and y)
time_data = stairs_data_t["Timestamp"]
x_data = stairs_data_t["X"]
y_data = stairs_data_t["Y"]
z_data = stairs_data_t["Z"]
pressure_data = stairs_data_t["Pressure"]

fig, ax1 = plt.subplots()
ax1.plot(time_data, x_data, label='acc_x', color=colors[0], linewidth=1.5)
ax1.plot(time_data, y_data, label='acc_y', color=colors[1], linewidth=1.5)
ax1.plot(time_data, z_data, label='acc_z', color=colors[2], linewidth=1.5)
ax1.set_xlabel('Time')
ax1.set_ylabel('Accelerometer')
ax1.set_ylim(min(x_data) - 1, max(y_data) + 1)

ax2 = ax1.twinx()

# Plot data on the secondary axis (right side)
ax2.plot(time_data, pressure_data, label='Pressure', color=colors[4], linewidth=3)
ax2.set_ylabel('Pressure')
ax2.set_ylim(min(pressure_data) - 0.5, max(pressure_data) + 0.75)

plt.title("Lift Down Class")

ax1.legend(handles=ax1.lines, labels=[l.get_label() for l in ax1.lines], loc='upper left')
plt.legend(handles=ax2.lines, labels=[l.get_label() for l in ax2.lines], loc='upper right')

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
plt.savefig("Lift Down Chart.pdf", bbox_inches="tight", pad_inches=0.5)

# Display the plot
plt.show()