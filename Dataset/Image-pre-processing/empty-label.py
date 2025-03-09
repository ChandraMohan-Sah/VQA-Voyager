import os

def check_empty_txt_files(folder_path):
    empty_files = []
    total_files = 0
    empty_count = 0

    # List all .txt files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            total_files += 1
            file_path = os.path.join(folder_path, file_name)
            
            # Check if file is empty
            if os.path.getsize(file_path) == 0:
                empty_files.append(file_name)
                empty_count += 1

    return total_files, empty_count, empty_files

if __name__ == "__main__":
    folder_path = 'D:\\Dataset-only\\annotated\\try-prayer wheel\\labels'  # Replace with your folder path
    total_files, empty_count, empty_files = check_empty_txt_files(folder_path)
    
    print(f"Total .txt files: {total_files}")
    print(f"Number of empty .txt files: {empty_count}")
    if empty_count > 0:
        print("Empty .txt files:")
        for file in empty_files:
            print(f" - {file}")
    else:
        print("No empty .txt files found.")
