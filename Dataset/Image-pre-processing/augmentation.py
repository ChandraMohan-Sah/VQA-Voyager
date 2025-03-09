import os
import cv2
import glob
import numpy as np
import albumentations as A

# Define augmentation pipeline
transform = A.Compose([
    A.OneOf([
        A.HorizontalFlip(p=0.5),  # 50% chance to apply horizontal flip
    ], p=1),  # Always apply one of the flips (only horizontal flip)
    A.OneOf([
        A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.5),  # Increased brightness and contrast limits
        A.RandomGamma(gamma_limit=(80, 120), p=0.5),  # Increased gamma range
    ], p=1),  # Always apply one of the color adjustments
    A.OneOf([
        A.GaussNoise(var_limit=(10.0, 50.0), p=0.7),  # Increased variance for Gaussian noise
        A.GaussianBlur(blur_limit=(1, 3), p=0.5),  # 50% chance to apply Gaussian blur with a blur limit between 1 and 3
    ], p=1),  # Always apply one of the noise or blur adjustments
    A.OneOf([
        A.Rotate(limit=15, p=0.5),  # 50% chance to apply rotation
    ], p=1)  # Always apply one of the spatial transformations
], bbox_params=A.BboxParams(format='yolo', label_fields=['category_ids']))

def load_image_and_labels(image_path, label_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    h, w = image.shape[:2]
    
    with open(label_path, 'r') as f:
        labels = f.readlines()
    
    bboxes = []
    category_ids = []
    for label in labels:
        class_id, x_center, y_center, width, height = map(float, label.strip().split())
        bboxes.append([x_center, y_center, width, height])
        category_ids.append(int(class_id))
    
    return image, bboxes, category_ids, h, w

def save_augmented_image_and_labels(augmented, image_path, label_path, output_image_dir, output_label_dir, count):
    base_name = os.path.basename(image_path).replace('.jpg', '')
    augmented_image = augmented['image']
    augmented_bboxes = augmented['bboxes']
    augmented_category_ids = augmented['category_ids']
    
    # Convert image back to BGR format for saving
    if isinstance(augmented_image, np.ndarray):
        augmented_image = cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR)
    
    # Save the augmented image
    augmented_image_path = os.path.join(output_image_dir, f"{base_name}_aug_{count}.jpg")
    cv2.imwrite(augmented_image_path, augmented_image)

    # Save the augmented labels
    augmented_label_path = os.path.join(output_label_dir, f"{base_name}_aug_{count}.txt")
    with open(augmented_label_path, 'w') as f:
        for bbox, category_id in zip(augmented_bboxes, augmented_category_ids):
            bbox_str = ' '.join(map(str, bbox))
            f.write(f"{category_id} {bbox_str}\n")

def augment_dataset(image_dir, label_dir, output_image_dir, output_label_dir, num_augmentations=6):
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)
    
    image_paths = glob.glob(os.path.join(image_dir, '*.jpg'))  # Assuming images are in .jpg format
    for image_path in image_paths:
        label_path = os.path.join(label_dir, os.path.basename(image_path).replace('.jpg', '.txt'))
        
        if not os.path.exists(label_path):
            continue
        
        image, bboxes, category_ids, h, w = load_image_and_labels(image_path, label_path)
        
        # Save the original image and labels
        save_augmented_image_and_labels({'image': image, 'bboxes': bboxes, 'category_ids': category_ids}, image_path, label_path, output_image_dir, output_label_dir, count=0)
        
        for i in range(1, num_augmentations + 1):
            augmented = transform(image=image, bboxes=bboxes, category_ids=category_ids)
            save_augmented_image_and_labels(augmented, image_path, label_path, output_image_dir, output_label_dir, count=i)

if __name__ == "__main__":
    image_dir = 'D:\\Dataset-only\\annotated\\yali\\images'
    label_dir = 'D:\\Dataset-only\\annotated\\yali\\labels'
    output_image_dir = 'D:\\Dataset-only\\annotated\\try-yali\\images'
    output_label_dir = 'D:\\Dataset-only\\annotated\\try-yali\\labels'
    
    augment_dataset(image_dir, label_dir, output_image_dir, output_label_dir)
