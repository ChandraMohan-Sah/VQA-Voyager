import os
import cv2
import glob
import numpy as np
import albumentations as A
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
        A.GaussianBlur(blur_limit=(1,3), p=0.5),  # 50% chance to apply Gaussian blur with a blur limit between 3 and 5
    ], p=1),  # Always apply one of the noise or blur adjustments
    A.OneOf([
        A.Rotate(limit=15, p=0.5),  # 50% chance to apply rotation
    ], p=1)  # Always apply one of the spatial transformations
], bbox_params=A.BboxParams(format='yolo', label_fields=['category_ids']))

def load_image_and_labels(image_path, label_path):
    image = cv2.imread(image_path)
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

def plot_bboxes(image, bboxes, categories, ax, color='r'):
    h, w = image.shape[:2]
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    for bbox, category in zip(bboxes, categories):
        x_center, y_center, width, height = bbox
        x_min = int((x_center - width / 2) * w)
        y_min = int((y_center - height / 2) * h)
        rect = Rectangle((x_min, y_min), width * w, height * h, linewidth=1, edgecolor=color, facecolor='none')
        ax.add_patch(rect)
        ax.text(x_min, y_min, str(category), color=color, fontsize=12, verticalalignment='top')

def display_images(original_image, original_bboxes, original_categories, augmented_images):
    n = len(augmented_images) + 1
    fig, axs = plt.subplots(1, n, figsize=(15, 7))
    
    # Original image with bounding boxes
    plot_bboxes(original_image, original_bboxes, original_categories, axs[0], color='r')
    axs[0].set_title('Original Image')
    
    # Augmented images with bounding boxes
    for i, (augmented_image, augmented_bboxes, augmented_categories) in enumerate(augmented_images):
        plot_bboxes(augmented_image, augmented_bboxes, augmented_categories, axs[i + 1], color='b')
        axs[i + 1].set_title(f'Augmented Image {i+1}')
    
    plt.show()

def augment_and_display(image_path, label_path, num_augmentations=3):
    image, bboxes, category_ids, h, w = load_image_and_labels(image_path, label_path)
    
    augmented_images = []
    for _ in range(num_augmentations):
        augmented = transform(image=image, bboxes=bboxes, category_ids=category_ids)
        augmented_image = augmented['image']
        augmented_bboxes = augmented['bboxes']
        augmented_category_ids = augmented['category_ids']
        
        # Convert augmented image to numpy array if it's not already
        if not isinstance(augmented_image, np.ndarray):
            augmented_image = augmented_image.permute(1, 2, 0).cpu().numpy()
            augmented_image = cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV
        
        augmented_images.append((augmented_image, augmented_bboxes, augmented_category_ids))

    display_images(image, bboxes, category_ids, augmented_images)

if __name__ == "__main__":
    image_dir = 'D:\\Dataset-only\\annotated\\yali\\images'
    label_dir = 'D:\\Dataset-only\\annotated\\yali\\labels'
    
    image_paths = glob.glob(os.path.join(image_dir, '*.jpg'))  # Assuming images are in .jpg format
    for image_path in image_paths:
        label_path = os.path.join(label_dir, os.path.basename(image_path).replace('.jpg', '.txt'))
        
        if not os.path.exists(label_path):
            continue
        
        augment_and_display(image_path, label_path, num_augmentations=3)
