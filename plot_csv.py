import matplotlib.pyplot as plt
import csv

# === Settings ===
csv_file = 'trial5.csv'

# === Data containers ===
time_vals = []
adc1_vals = []
adc2_vals = []

# === Read CSV ===
with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    header = next(reader)  # Read header row

    title_adc1 = header[1]
    title_adc2 = header[2]

    for row in reader:
        time_vals.append(float(row[0]))
        adc1_vals.append(int(row[1]))
        adc2_vals.append(int(row[2]))

# === Plotting ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)

ax1.plot(time_vals, adc1_vals, color='r')
ax1.set_title(title_adc1)
ax1.set_ylabel("ADC Value")
ax1.set_ylim(0, 4100)
ax1.grid(True)

ax2.plot(time_vals, adc2_vals, color='g')
ax2.set_title(title_adc2)
ax2.set_ylabel("ADC Value")
ax2.set_xlabel("Time (s)")
ax2.set_ylim(0, 4100)
ax2.grid(True)

plt.tight_layout()
plt.show()
