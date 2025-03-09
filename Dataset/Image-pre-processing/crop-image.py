import cv2
import os

# Define the input and output directories
input_directory = "D:\\Dataset-only\\prayer-wheel-resized"
output_directory = "D:\\Dataset-only\\prayer-wheel-cropped"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# List all image files in the input directory
image_files = [f for f in os.listdir(input_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Process each image file
for image_file in image_files:
    # Load the image
    image_path = os.path.join(input_directory, image_file)
    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        print(f"Error loading image: {image_path}")
        continue

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Define the cropping region (assuming the watermark is at the bottom)
    # Here, we'll crop 50 pixels from the bottom of the image. Adjust as necessary.
    crop_height = height - 30

    # Crop the image
    cropped_image = image[:crop_height, :]

    # Save the cropped image in the output directory
    output_path = os.path.join(output_directory, f"cropped_{image_file}")
    cv2.imwrite(output_path, cropped_image)

    # Display the cropped image (optional)
    cv2.imshow("Cropped Image", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"Cropped image saved at {output_path}")
