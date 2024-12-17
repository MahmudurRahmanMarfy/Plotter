import serial
import re
import pandas as pd
from datetime import datetime
import os  # For folder management

# Config
SERIAL_PORT = "COM6"  # Ensure COM6 is correct for your device
BAUD_RATE = 9600

def generate_filename():
    """
    Generate a dynamic filename based on the current date and time.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = "data"
    if not os.path.exists(folder):  # Create the folder if it doesn't exist
        os.makedirs(folder)
    return f"{folder}/serial_data_{timestamp}.csv"

def save_to_csv(data, filename):
    """
    Save collected data to a CSV file using pandas.
    """
    try:
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)
        # Save to CSV
        df.to_csv(filename, index=False)
        print(f"[INFO] Data successfully saved to {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to save data to {filename}: {e}")

def main(serial_port, baud_rate):
    data_records = []
    save_file = generate_filename()
    
    try:
        # Open serial connection
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"[SUCCESS] Connected to {serial_port} at {baud_rate} baud")
        print("[INFO] Listening for incoming data...")
    except Exception as e:
        print(f"[ERROR] Failed to connect to {serial_port} at {baud_rate} baud.\n[ERROR] {e}")
        return

    print("[INFO] Incoming data... Press Ctrl+C to stop.")
    
    try:
        while True:
            if ser.in_waiting > 0:
                line_data = ser.readline().decode("utf-8").strip()
                print(line_data)

                # Regex to capture keys and numeric values (integer or floating-point)
                pairs = re.findall(r"([\w\.\[\]um_]+):(-?\d+(?:\.\d+)?)", line_data)

                # Convert the parsed pairs into a dictionary
                data_dict = {key: float(value) if '.' in value else int(value) for key, value in pairs}
                
                # Add a timestamp to the dictionary
                data_dict['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Add the dictionary to the list
                if data_dict:  # Only add non-empty dictionaries
                    data_records.append(data_dict)
    except KeyboardInterrupt:
        print(f"[INFO:KeyboardInterrupt] Closing connection to {serial_port}")
    finally:
        # Save data to a CSV file
        if data_records:
            print(f"[INFO] Saving data to {save_file}")
            save_to_csv(data_records, save_file)
        else:
            print("[INFO] No data to save.")
        ser.close()
        print(f"[INFO] Connection to {serial_port} closed")

if __name__ == "__main__":
    main(SERIAL_PORT, BAUD_RATE)
