import os

def rename_images_in_folder(folder_path):
    count = 1
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            new_filename = f"akhi_jhyal_L_{count:02}.jpg"
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")
            
            count += 1
        else:
            print(f"Skipping non-image file {filename}")

folder_path = 'D:\\Dataset-only\\akhi jhyal-looza\\Akhi jhyal'
rename_images_in_folder(folder_path)
