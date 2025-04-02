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

def list_files(directory):
    files = glob.glob(os.path.join(directory, '*.csv'))
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
    plt.title(f'Current Over Time (All Phases) {df["timestamp"].min()} - {df["timestamp"].max()}')
    plt.legend()
    plt.grid()
    plt.savefig(f"{os.path.splitext(csv_file)[0]}_current_graph_all_phases.png")
    

def merge_files_per_day():
    data_by_date = {}
    for file in list_files(defaault_path):

        print(f"Processing file: {file}")
        df = pd.read_csv(file)
        df['date'] = pd.to_datetime(df['timestamp'], unit='s').dt.date
        
        for date, group in df.groupby('date'):
            date_str = date.strftime('%Y-%m-%d')
            
            if date_str in data_by_date:
                data_by_date[date_str] = pd.concat([data_by_date[date_str], group], ignore_index=True)
            else:
                data_by_date[date_str] = group

    for date_str, data in data_by_date.items():
        data = data.drop(columns=['date'])
        output_folder = os.path.join(defaault_path, date_str)
        os.makedirs(output_folder, exist_ok=True)
        
        output_file = os.path.join(output_folder, f"{date_str}.csv")
        data.to_csv(output_file, index=False)
        print(f"Saved merged file: {output_file}")

# Запуск функции
merge_files_per_day()
create_voltage_graph_from_csv_file('/Volumes/NetworkBackupShare/shelly/2025-04-02/2025-04-02.csv')
create_current_graph_from_csv_file('/Volumes/NetworkBackupShare/shelly/2025-04-02/2025-04-02.csv')

for file in list_files('/Volumes/NetworkBackupShare/shelly'):
    print(file)
    with open(file, 'r') as f:
        file_contents = f.read()
        #print(file_contents)
        create_voltage_graph_from_csv_file(file)
        create_current_graph_from_csv_file(file)
        time.sleep(1)
