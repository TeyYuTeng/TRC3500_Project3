import matplotlib.pyplot as plt
import time
import csv
import os

def moving_average(signal, window_size=5):
    """Applies a simple moving average filter to the signal."""
    return [sum(signal[i:i+window_size])/window_size if i+window_size <= len(signal) else signal[i]
            for i in range(len(signal))]

def threshold_peak_detector(signal, threshold):
    """
    Detects peaks in a signal based on threshold crossing:
    A peak is counted when the signal rises above the threshold and
    then falls below it.
    """
    peaks = []
    above = False

    for i in range(1, len(signal)):
        if not above and signal[i] > threshold:
            above = True
        elif above and signal[i] <= threshold:
            peaks.append(i)
            above = False

    return peaks

# === Settings ===
csv_file = 'test.csv'
time_window = 30
sample_interval = 0.1  # seconds per sample
num_samples = int(time_window/sample_interval)

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

    # Apply moving average filter
    filtered_adc1 = moving_average(adc1_vals, window_size=5)
    filtered_adc2 = moving_average(adc2_vals, window_size=5)

    # Thermistor
    threshold1 = (max(filtered_adc1) + min(filtered_adc1))/2
    peaks1 = threshold_peak_detector(filtered_adc1, threshold1)
    est_rate_1 = (len(peaks1) * 60) / (num_samples * sample_interval)

    print("=========== Thermistor Sensor ==========")
    print(f"Estimated rate: {est_rate_1:.1f} bpm")
    print(f"Peaks detected: {len(peaks1)}\n")

    # Conductive band Sensor
    threshold2 = (max(filtered_adc2) + min(filtered_adc2))/2
    peaks2 = threshold_peak_detector(filtered_adc2, threshold2)
    est_rate_2 = (len(peaks2) * 60) / (num_samples * sample_interval)

    print("=========== Conductive band Sensor ==========")
    print(f"Estimated rate: {est_rate_2:.1f} bpm")
    print(f"Peaks detected: {len(peaks2)}\n")

    weight1 = 0.5  # confidence in thermistor
    weight2 = 1 - weight1  # confidence in conductive band

    fused_bpm = (weight1 * est_rate_1) + (weight2 * est_rate_2)

    print("=========== Final BPM ==========")
    print(f"Estimated rate (fused): {round(fused_bpm)} bpm")

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
