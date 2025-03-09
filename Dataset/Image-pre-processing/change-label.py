import os
import re

def modify_first_numbers_in_files(folder_path, new_number):
    # Regex pattern to match the first number before a space
    pattern = re.compile(r'^(\d+)\s')
    
    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            
            # Read the file content
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Modify the first number in each line
            modified_lines = []
            for line in lines:
                modified_line = pattern.sub(f'{new_number} ', line)
                modified_lines.append(modified_line)
            
            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.writelines(modified_lines)

# Specify the folder containing the .txt files
folder_path = 'D:\\Dataset-only\\annotated\\akhi jhyal\\labels'
# Specify the new number to replace the first number in each line
new_number = '1'

# Call the function to modify the first numbers in the files
modify_first_numbers_in_files(folder_path, new_number)

print(f'First numbers in each line of all .txt files in {folder_path} have been modified to {new_number}.')
