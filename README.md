# Energy Management Scripts

This repository contains scripts and tools for managing and monitoring energy consumption using Shelly EM3 Pro devices. The main script converts JSON data from Shelly devices to CSV format for further analysis and storage.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.6+
- `requests` library
- `pandas` library

## Installation

To set up the environment and install the required packages, run:

```
pip install requests pandas
```

## Usage

The main script shelly_em3pro_json_to_csv_converter.py fetches data from a Shelly EM3 Pro device and converts it to a CSV file. The CSV files are stored in the specified output directory with hourly rotation.
Running the Script

To run the script, execute:
```
python shelly_em3pro_json_to_csv_converter.py
```

## Script Details

* The script fetches data from a Shelly EM3 Pro device using its IP address.
* It adds a Unix timestamp to the data.
* The data is converted to a Pandas DataFrame, and the 'id' column (if it exists) is dropped.
* The script generates a CSV file with the timestamp as the first column and stores it in the specified output directory.
* If the CSV file exists, the script appends the new data to it; otherwise, it creates a new file with headers.

## Configuration

The script needs the following configuration:

 * Shelly IP Address: Set the IP address of your Shelly device in the shelly_ip variable.
 * Output Directory: Set the output directory where the CSV files will be stored in the output_dir variable.


# Example configuration

```
output_dir = r"/mnt/NetworkBackupShare/shelly"
shelly_ip = "192.168.10.69"
```

Contributing

Contributions are welcome! Please follow these steps to contribute:

    * Fork the repository.
    * Create a new branch with your feature or bug fix.
    * Commit your changes and push the branch to your forked repository.
    * Create a pull request with a detailed description of your changes.

License

This project is licensed under the MIT License. See the LICENSE file for details.
