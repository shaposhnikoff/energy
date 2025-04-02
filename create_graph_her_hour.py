import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

import os
import glob
import re
import sys
import shutil
import json
import time
import logging
import requests
import math
import statistics
import random
import string
import csv

defaault_path = '/Volumes/NetworkBackupShare/shelly'
#iterate over the list of files shellyStats
# list all the files in the directory
def list_files(directory):
    # Use glob to find all files in the directory
    files = glob.glob(os.path.join(directory, '*'))
    return files

def create_voltage_graph_from_csv_file(csv_file):
    # Create a voltage graph from the CSV file
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Convert the timestamp from Unix time to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Plot the voltage over time for all three phases
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['a_voltage'], label='Phase A Voltage', color='blue')
    plt.plot(df['timestamp'], df['b_voltage'], label='Phase B Voltage', color='green')
    plt.plot(df['timestamp'], df['c_voltage'], label='Phase C Voltage', color='red')
    
    plt.xlabel('Time')
    plt.ylabel('Voltage (V)')
    plt.title(f'Voltage Over Time (All Phases) {df["timestamp"].min()} - {df["timestamp"].max()}')

    plt.legend()
    plt.grid()
    
    # Save the plot to a file
    plt.savefig(f"{os.path.splitext(csv_file)[0]}_voltage_graph_all_phases.png")

def create_current_graph_from_csv_file(csv_file):
    # Create a voltage graph from the CSV file
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Convert the timestamp from Unix time to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Plot the voltage over time for all three phases
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['a_current'], label='Phase A Current', color='blue')
    plt.plot(df['timestamp'], df['b_current'], label='Phase B Current', color='green')
    plt.plot(df['timestamp'], df['c_current'], label='Phase C Current', color='red')
    
    plt.xlabel('Time')
    plt.ylabel('Current (A)')
    #plt.title('Current Over Time (All Phases)')
    # make title with timeperiod
    plt.title(f'Current Over Time (All Phases) {df["timestamp"].min()} - {df["timestamp"].max()}')
    plt.legend()
    plt.grid()
    
    # Save the plot to a file
    plt.savefig(f"{os.path.splitext(csv_file)[0]}_current_graph_all_phases.png")
    

for file in list_files('/Volumes/NetworkBackupShare/shelly'):
    print(file)
    with open(file, 'r') as f:
        file_contents = f.read()
        #print(file_contents)
        create_voltage_graph_from_csv_file(file)
        create_current_graph_from_csv_file(file)
        time.sleep(1)
