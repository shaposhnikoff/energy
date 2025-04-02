import requests
import datetime
import os
import pandas as pd

# Output directory
output_dir = r"/mnt/NetworkBackupShare/shelly"
os.makedirs(output_dir, exist_ok=True)

shelly_ip = "192.168.10.69"

base_url = f"http://{shelly_ip}"
print(f"Device found at {base_url}")
try:
    # Fetch data from the Shelly device
    status = requests.get(f"{base_url}/rpc/Shelly.GetStatus", timeout=2).json()
    shelly_status = status['em:0']
    
    # Add a Unix timestamp to the data
    shelly_status["timestamp"] = int(datetime.datetime.now().timestamp())
    
    # Convert the data to a pandas DataFrame
    shelly_status_df = pd.DataFrame([shelly_status])
    
    # Drop the 'id' column if it exists
    if 'id' in shelly_status_df.columns:
        shelly_status_df = shelly_status_df.drop(columns=['id'])
    
    # Reorder columns to make 'timestamp' the first column
    columns = ['timestamp'] + [col for col in shelly_status_df.columns if col != 'timestamp']
    shelly_status_df = shelly_status_df[columns]
    
    # Define the CSV file path with hourly rotation
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H")  # Include the hour in the file name
    csv_file = os.path.join(output_dir, f"shellyStatus_{timestamp}.csv")
    
    # Check if the file exists
    if os.path.exists(csv_file):
        # Append to the existing file
        shelly_status_df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        # Create a new file with headers
        shelly_status_df.to_csv(csv_file, index=False)
    
    print(f"Data received from {shelly_ip}: {shelly_status}")
    print(f"CSV file updated at: {csv_file}")
except requests.exceptions.RequestException as e:
    print(f"Failed to get data from {shelly_ip}: {e}")
except KeyError as e:
    print(f"Unexpected data format: missing key {e}")
