import serial
import matplotlib.pyplot as plt
import time
import csv

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

# ======================
# Settings
# ======================
file_name ='test'
num_samples = 100
sample_interval = 0.1  # seconds per sample

adc1 = []
adc2 = []

# Serial setup
ser = serial.Serial('COM4', 115200, timeout=1)
print("====================")
print(f"Collecting {num_samples} samples...")

start_time = time.time()

try:
    while len(adc1) < num_samples:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line.startswith("ADC:"):
                try:
                    parts = line.replace("ADC:", "").strip().split(",")
                    if len(parts) == 2:
                        v1 = int(parts[0].strip())
                        v2 = int(parts[1].strip())

                        adc1.append(v1)
                        adc2.append(v2)
                except ValueError:
                    print(f"Invalid data: {line}")

    elapsed = time.time() - start_time
    print(f"Finished collecting {num_samples} samples in {elapsed:.2f} seconds.")

    x = [i * sample_interval for i in range(num_samples)]

    # Save to CSV
    with open(f'{file_name}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Thermistor', 'Conductive Band'])
        for i in range(num_samples):
            writer.writerow([x[i], adc1[i], adc2[i]])
    print(f"Data saved to {file_name}.csv\n")

    # Thermistor
    threshold1 = 1100
    peaks1 = threshold_peak_detector(adc1, threshold1)
    est_rate_1 = (len(peaks1) * 60) / (num_samples * sample_interval)

    print("=========== Thermistor Sensor ==========")
    print(f"Estimated rate: {est_rate_1:.1f} bpm")
    print(f"Peaks detected: {len(peaks1)}\n")

    # Conductive band Sensor
    threshold2 = 1000
    peaks2 = threshold_peak_detector(adc2, threshold2)
    est_rate_2 = (len(peaks2) * 60) / (num_samples * sample_interval)

    print("=========== Conductive band Sensor ==========")
    print(f"Estimated rate: {est_rate_2:.1f} bpm")
    print(f"Peaks detected: {len(peaks2)}\n")

    avg = (est_rate_1 + est_rate_2) / 2

    print("=========== Average ==========")
    print(f"Estimated rate: {avg} bpm\n")

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), sharex=True)

    ax1.plot(x, adc1, color='r')
    ax1.set_ylim(0, 4100)
    ax1.set_title("Thermistor")
    ax1.set_ylabel("ADC Value")
    ax1.grid(True)

    ax2.plot(x, adc2, color='g')
    ax2.set_ylim(0, 4100)
    ax2.set_title("Conductive band")
    ax2.set_ylabel("ADC Value")
    ax2.set_xlabel("Time (s)")
    ax2.grid(True)

    ax1.set_xlim(0, num_samples * sample_interval)

    plt.tight_layout()
    plt.show()

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    ser.close()
