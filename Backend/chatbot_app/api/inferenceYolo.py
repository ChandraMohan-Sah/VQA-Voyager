# import os
# from ultralytics import YOLO

# # Load YOLO model
# MODEL_PATH = os.path.join(os.getcwd(), 'best.pt')
# model = YOLO(MODEL_PATH)

# def run_inference(image_path, output_dir):
#     """
#     Runs YOLO inference on the given image and saves the result.

#     Args:
#         image_path (str): Path to the input image.
#         output_dir (str): Directory to save the result image.

#     Returns:
#         str: Path to the result image.
#         list: Detected objects with labels and confidence scores.
#     """
#     os.makedirs(output_dir, exist_ok=True)

#     # Run YOLO inference
#     results = model([image_path])
#     result_image_path = os.path.join(output_dir, f"result_{os.path.basename(image_path)}")
#     results[0].save(filename=result_image_path)

#     # Extract detected objects (label and confidence)
#     detected_objects = []
#     for box in results[0].boxes:
#         label = box.data[0][-1]  # Label index
#         score = box.data[0][-2]  # Confidence score
#         detected_objects.append({
#             'label': model.names[int(label)],
#             'score': f"{score:.2f}"
#         })

#     return result_image_path, detected_objects



import os
from ultralytics import YOLO
import time  # Import the time module for profiling

# Load YOLO model
MODEL_PATH = os.path.join(os.getcwd(), 'best.pt')
model = YOLO(MODEL_PATH)

def run_inference(image_path, output_dir):
    """
    Runs YOLO inference on the given image and saves the result.

    Args:
        image_path (str): Path to the input image.
        output_dir (str): Directory to save the result image.

    Returns:
        str: Path to the result image.
        list: Detected objects with labels and confidence scores.
    """

    os.makedirs(output_dir, exist_ok=True)

    # Start measuring the inference time
    inference_start_time = time.time()

    # Run YOLO inference
    results = model([image_path])

    # Time taken for YOLO inference
    inference_time = time.time() - inference_start_time
    print(f"YOLO Inference Time: {inference_time:.4f} seconds")

    result_image_path = os.path.join(output_dir, f"result_{os.path.basename(image_path)}")
    results[0].save(filename=result_image_path)

    # Start measuring the detection extraction time
    detection_start_time = time.time()

    # Extract detected objects (label and confidence)
    detected_objects = []
    for box in results[0].boxes:
        label = box.data[0][-1]  # Label index
        score = box.data[0][-2]  # Confidence score
        detected_objects.append({
            'label': model.names[int(label)],
            'score': f"{score:.2f}"
        })

    # Time taken for extracting detected objects
    detection_time = time.time() - detection_start_time
    print(f"Object Extraction Time: {detection_time:.4f} seconds")

    # Calculate total time taken
    total_time = time.time() - inference_start_time
    print(f"Total Time (Inference + Object Extraction): {total_time:.4f} seconds")

    return result_image_path, detected_objects
