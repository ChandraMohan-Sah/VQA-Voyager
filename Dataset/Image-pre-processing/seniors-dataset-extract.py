import os
import shutil

# Set the path to your dataset
dataset_path = 'D:/Major Project/senior-dataset'
output_path = 'D:/Major Project/output-dataset'
class_to_extract = 37

# Function to create output directories if they don't exist
def create_output_dirs(base_path):
    if not os.path.exists(base_path):
        os.makedirs(base_path)

# Create output directories for images and labels
create_output_dirs(os.path.join(output_path, 'images'))
create_output_dirs(os.path.join(output_path, 'labels'))

# Function to filter and copy images and labels for a specific dataset split
def filter_and_copy(split, class_to_extract):
    images_dir = os.path.join(dataset_path, 'images', split)
    labels_dir = os.path.join(dataset_path, 'labels', split)
    output_images_dir = os.path.join(output_path, 'images')
    output_labels_dir = os.path.join(output_path, 'labels')

    for label_file in os.listdir(labels_dir):
        label_path = os.path.join(labels_dir, label_file)
        
        # Check if the current path is a file
        if os.path.isfile(label_path):
            # Read the label file
            with open(label_path, 'r') as file:
                lines = file.readlines()
            
            # Filter lines for the specified class
            filtered_lines = [line for line in lines if int(line.split()[0]) == class_to_extract]
            
            if filtered_lines:
                print(f"Processing {label_file}, found class {class_to_extract}")
                # Copy the label file with filtered content
                output_label_path = os.path.join(output_labels_dir, label_file)
                with open(output_label_path, 'w') as file:
                    file.writelines(filtered_lines)
                
                # Copy the corresponding image file
                image_file = label_file.replace('.txt', '.jpg')
                image_path = os.path.join(images_dir, image_file)
                if os.path.exists(image_path):
                    shutil.copy(image_path, os.path.join(output_images_dir, image_file))
                else:
                    print(f"Image file {image_file} not found for {label_file}")

# Process each split: train, test, val
for split in ['train', 'test', 'val']:
    filter_and_copy(split, class_to_extract)

print("Extraction completed.")
