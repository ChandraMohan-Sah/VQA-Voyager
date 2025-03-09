import os
from collections import defaultdict

# Path to the folder containing the .txt files
folder_path = 'D:\\Dataset-only\\dataset-part-A'

# Dictionary to hold the counts of each number
number_counts = defaultdict(int)

# Walk through the folder and subfolders
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith('.txt'):
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as file:
                # Read each line in the file
                for line in file:
                    # Extract the number at the beginning of the line
                    parts = line.split()
                    if parts and parts[0].isdigit():
                        number = int(parts[0])
                        number_counts[number] += 1

# Print the counts of each number
for number, count in number_counts.items():
    print(f'Number {number} occurs {count} times')
