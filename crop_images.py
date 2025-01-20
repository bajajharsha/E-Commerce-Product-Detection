import cv2
import os
import time

def crop_image(image_path, output_folder):
    try:
        num_parts = 8
        img = cv2.imread(image_path)                    # Read the image
        img_height, img_width, _ = img.shape            # Get the image dimensions
        img_height, img_width, _ = img.shape            # Get the image dimensions
        part_height = img_height // num_parts           # Calculate the height of each part
        counter = 1     
        
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  # Initialize a counter for naming the cropped images     

        # Loop through the image and crop it into smaller parts
        for i in range(num_parts):
            y_start = i * part_height                       # Calculate the starting y-coordinate
            y_end = (i + 1) * part_height if i != num_parts - 1 else img_height         # Calculate the ending y-coordinate
            cropped_img = img[y_start:y_end, 0:img_width]   # Crop the image

            # Save the cropped image
            cropped_image_path = os.path.join(output_folder, f"cropped_{os.path.basename(image_path).split('.')[0]}_{counter}.png")
            cv2.imwrite(cropped_image_path, cropped_img)
            counter += 1

        # print(f"Cropping completed for {image_path}. Cropped images are saved in '{output_folder}'.")

    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def get_images(input_folder, output_folder):
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):                                                           # Iterate through all files in the input folder         
        file_path = os.path.join(input_folder, filename)                                                # Get the full file path
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):          # Check if the file is an image
            crop_image(file_path, output_folder)
