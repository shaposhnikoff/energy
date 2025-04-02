def create_html_with_graphs(graph_folder, output_html):
    """
    Iterate over all files in the specified folder and create an HTML file with embedded graphs.
    
    :param graph_folder: Path to the folder containing graph images.
    :param output_html: Path to the output HTML file.
    """
    # List all PNG files in the folder
    graph_files = sorted(glob.glob(os.path.join(graph_folder, '*.png')))
    
    # Start building the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Graphs Overview</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { text-align: center; }
            .graph { margin-bottom: 20px; text-align: center; }
            img { max-width: 100%; height: auto; border: 1px solid #ddd; padding: 5px; }
        </style>
    </head>
    <body>
        <h1>Graphs Overview</h1>
    """
    
    # Add each graph to the HTML
    for graph_file in graph_files:
        graph_name = os.path.basename(graph_file)
        html_content += f"""
        <div class="graph">
            <h2>{graph_name}</h2>
            <img src="{graph_file}" alt="{graph_name}">
        </div>
        """
    
    # Close the HTML content
    html_content += """
    </body>
    </html>
    """
    
    # Write the HTML content to the output file
    with open(output_html, 'w') as html_file:
        html_file.write(html_content)
    
    print(f"HTML file created: {output_html}")

# Example usage
create_html_with_graphs('/Volumes/NetworkBackupShare/shelly/Graph', '/Volumes/NetworkBackupShare/shelly/graphs_overview.html')
