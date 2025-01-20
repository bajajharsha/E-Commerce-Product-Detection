import os
import cv2

def save_segmented_objects(result, image, filename):
    """
    Segments detected objects from the image and saves them into separate files.

    Args:
        result: YOLO result object containing bounding boxes and detection info.
        image: Original image as a numpy array.
        filename: Original image filename.
    """
    
    segmented_folder = "segmented_objects"
    os.makedirs(segmented_folder, exist_ok=True)  # Create the segmented objects folder if it doesn't exist
    
    for idx, (box, cls) in enumerate(zip(result.boxes.xyxy, result.boxes.cls)):  # Iterate through detected boxes
        x_min, y_min, x_max, y_max = map(int, box)  # Get coordinates of the bounding box
        cropped_object = image[y_min:y_max, x_min:x_max]  # Crop the object from the image
        
        class_name = result.names[int(cls)]
        class_folder = os.path.join(segmented_folder, class_name)
        os.makedirs(class_folder, exist_ok=True)  # Create a folder for each class if it doesn't exist
        
        # Create a filename for the cropped object
        base_filename = os.path.splitext(filename)[0]
        segmented_filename = f"{base_filename}_{class_name}_{idx}.jpg"
        segmented_path = os.path.join(class_folder, segmented_filename)

        cv2.imwrite(segmented_path, cropped_object)  # Save the cropped object
        # print(f"Saved segmented object to {segmented_path}")