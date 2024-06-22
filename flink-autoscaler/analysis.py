import os
import re
import subprocess
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_options(output):
    """
    Parses the output from the Java command to extract configuration options and their descriptions.
    Each option is followed by its description on the next line.
    """
    print(output)
    lines = [line.strip() for line in output.split('\n') if line.strip()]
    options = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('key:'):
            option = lines[i][len('key: '):]  # Remove the 'key: ' prefix
            description = lines[i+1][len('description: '):] if i+1 < len(lines) and lines[i+1].startswith('description:') else "No description available"
            options.append({'option': option, 'description': description})
            i += 2
        else:
            i += 1
    return options

if __name__ == "__main__":
    class_to_commands = {'KubernetesOperatorConfigOptions':
        [
        "java",
        "@cp_5jrxtqk4s0lusb0xwljbrs2rd.argfile",
        "org.apache.flink.kubernetes.operator.config.AnalyzeOptions",
        "org.apache.flink.kubernetes.operator.config.KubernetesOperatorConfigOptions"
    ], 'AutoscalerOptions':[
        "java",
        "@cp_c5qa97urasm0zbc2tww5w3rul.argfile",
        "org.apache.flink.autoscaler.config.AnalyzeOptions",
        "org.apache.flink.autoscaler.config.AutoScalerOptions"
    ] 
    }

    # Open the CSV file to write the results
    for class_name, command in class_to_commands.items():
        with open(class_name + '_config_options.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Config Option', 'Description'])  # Write header

            try:
                # Execute the Java command
                result = subprocess.run(command, check=True, capture_output=True, text=True)

                # Parse the output to get the list of options with descriptions
                options = parse_options(result.stdout)
                
                # Write to CSV
                for option in options:
                    csv_writer.writerow([option['option'], option['description']])
                csvfile.flush()  # Ensure data is written to the file
                
            except subprocess.CalledProcessError as e:
                logging.error(f"Error processing: {e.stderr}")
                # Write error to CSV
                csv_writer.writerow([f"Error: {e.stderr}", ""])
                csvfile.flush()  # Ensure data is written to the file

            logging.info("------------------------")

            logging.info("CSV file has been created with the results.")

