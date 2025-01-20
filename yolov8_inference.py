import os
import cv2
from ultralytics import YOLO
import time
import shutil
from segment_objects import save_segmented_objects 
from concurrent.futures import ProcessPoolExecutor, as_completed

# Load the pre-trained YOLOv8 model outside the processing function
model = YOLO("model/trained_yolov8n_model.pt")

def process_image(file_path, output_folder, model):
    image = cv2.imread(file_path)                                                                               # Read the image using OpenCV
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)                                                          # Convert the image from BGR to RGB
    results = model(image_rgb)                                                                                  # Run the YOLOv8 model on the image
    result = results[0]                                                                                         # Get the first result object
    result_image = result.plot()                                                                                # Draw the bounding boxes on the image
    result_image_bgr = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)                                            # Convert to BGR
    filename = os.path.basename(file_path)
    output_path = os.path.join(output_folder, f"result_{filename}")                                             # Path for output image
    cv2.imwrite(output_path, result_image_bgr)                                                                  # Save the processed image

    # Save segmented objects
    print(f"Processing {filename}")
    save_segmented_objects(result, image, filename)  # Segment and save detected objects

def run_yolov8_on_images(input_folder, output_folder, batch_size=5, max_workers=8):
    os.makedirs(output_folder, exist_ok=True)                                                                   # Create the output folder if it doesn't exist
    file_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder)]                # List all files in the input folder
    batches = [file_paths[i:i + batch_size] for i in range(0, len(file_paths), batch_size)]                     # Batch processing: Divide images into batches
    
    # Use ProcessPoolExecutor to parallelize the processing
    print("Processing images...")
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for batch in batches:
            for file_path in batch:
                futures.append(executor.submit(process_image, file_path, output_folder, model))  # Submit each task individually

        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()  # Retrieve the result to ensure any exceptions are raised
            except Exception as e:
                print(f"Error processing image: {e}")
            # Process each batch in parallel using executor

    shutil.rmtree("dataset")
    shutil.rmtree("async_dataset")
    shutil.rmtree("final_output")

# Example usage:
# if __name__ == "__main__":
#     input_folder = "dataset"
#     output_folder = "final_output"
#     start_time = time.time()
#     run_yolov8_on_images(input_folder, output_folder)
#     end_time = time.time()
#     print(f"Time taken: {end_time - start_time:.2f} seconds")
