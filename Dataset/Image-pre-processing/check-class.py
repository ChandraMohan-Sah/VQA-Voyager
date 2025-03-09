import os
import re
from collections import defaultdict

def find_first_numbers_in_files(folder_path):
    # Dictionary to store the counts of each first number
    first_number_counts = defaultdict(int)
    
    # Regex pattern to match the first number before a space
    pattern = re.compile(r'^(\d+)\s')
    
    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as file:
                for line in file:
                    match = pattern.match(line)
                    if match:
                        first_number = match.group(1)
                        first_number_counts[first_number] += 1
    
    return first_number_counts

# Specify the folder containing the .txt files
folder_path = 'D:\\Dataset-only\\annotated\\akhi jhyal\\labels'

# Call the function and print the results
first_number_counts = find_first_numbers_in_files(folder_path)

for number, count in first_number_counts.items():
    print(f'Number {number} occurs {count} times as the first number in a line before a space.')
