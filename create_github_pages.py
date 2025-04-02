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


def create_readme_with_graphs(graph_folder, output_readme):
    """
    Iterate over all files in the specified folder and create a README.md file with embedded graphs.
    
    :param graph_folder: Path to the folder containing graph images.
    :param output_readme: Path to the output README.md file.
    """
    # List all PNG files in the folder
    graph_files = sorted(glob.glob(os.path.join(graph_folder, '*.png')))
    
    # Start building the README content
    readme_content = "# Graphs Overview\n\n"
    
    # Add each graph to the README
    for graph_file in graph_files:
        graph_name = os.path.basename(graph_file)
        readme_content += f"## {graph_name}\n"
        readme_content += f"![{graph_name}](graph/{graph_name})\n\n"
    
    # Write the README content to the output file
    with open(output_readme, 'w') as readme_file:
        readme_file.write(readme_content)
    
    print(f"README.md file created: {output_readme}")

# Example usage
create_readme_with_graphs('graph', 'README.md')