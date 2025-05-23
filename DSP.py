import serial
import matplotlib.pyplot as plt
import time  # <-- import time module

# Arrays to store ADC values
adc1 = []
adc2 = []
adc3 = []

# Serial setup
ser = serial.Serial('COM4', 115200, timeout=1)

print("Collecting 100 samples...")

start_time = time.time()  # <-- start timer

try:
    while len(adc1) < 100:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line.startswith("ADC:"):
                try:
                    parts = line.replace("ADC:", "").strip().split(",")
                    if len(parts) == 3:
                        v1 = int(parts[0].strip())
                        v2 = int(parts[1].strip())
                        v3 = int(parts[2].strip())

                        adc1.append(v1)
                        adc2.append(v2)
                        adc3.append(v3)
                except ValueError:
                    print(f"Invalid data: {line}")

    elapsed = time.time() - start_time  # <-- calculate elapsed time
    print(f"Finished collecting 100 samples in {elapsed:.2f} seconds. Plotting final graph...")

    # Prepare x-axis 0 to 5 for 100 samples
    x = [i * 5 / 99 for i in range(100)]

    # Plot setup: 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6), sharex=True)

    ax1.plot(x, adc1[::-1], color='r')
    ax1.set_ylim(0, 4100)
    ax1.set_title("ADC1")
    ax1.set_ylabel("ADC Value")
    ax1.grid(True)

    ax2.plot(x, adc2[::-1], color='g')
    ax2.set_ylim(0, 4100)
    ax2.set_title("ADC2")
    ax2.set_ylabel("ADC Value")
    ax2.grid(True)

    ax3.plot(x, adc3[::-1], color='b')
    ax3.set_ylim(0, 4100)
    ax3.set_title("ADC3")
    ax3.set_ylabel("ADC Value")
    ax3.set_xlabel("Time (s)")
    ax3.grid(True)

    ax1.set_xlim(0, 5)

    plt.tight_layout()
    plt.show()

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    ser.close()
