import os

def delete_images_and_txt_files(image_filenames, image_folder, txt_folder):
    for image_filename in image_filenames:
        # Construct full image file path
        image_file_path = os.path.join(image_folder, image_filename)
        
        # Get the base name without extension
        base_name = os.path.splitext(image_filename)[0]
        txt_filename = base_name + '.txt'
        txt_file_path = os.path.join(txt_folder, txt_filename)
        
        # Check if the image file exists and delete it
        if os.path.exists(image_file_path):
            os.remove(image_file_path)
            print(f"Deleted image {image_file_path}")
        else:
            print(f"{image_file_path} does not exist")
        
        # Check if the .txt file exists and delete it
        if os.path.exists(txt_file_path):
            os.remove(txt_file_path)
            print(f"Deleted txt file {txt_file_path}")
        else:
            print(f"{txt_file_path} does not exist")

# Example usage
image_filenames = ['ujj-al (634).jpg', 'rishav (36).jpg']
image_folder = 'D:\Dataset-only\senior-extracted-dataset\class_42 (Taleju Temple)\images'
txt_folder = 'D:\Dataset-only\senior-extracted-dataset\class_42 (Taleju Temple)\labels'
delete_images_and_txt_files(image_filenames, image_folder, txt_folder)


