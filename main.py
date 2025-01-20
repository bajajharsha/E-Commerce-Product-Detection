import asyncio
import time
from async_capture import generate_urls, capture_multiple_screenshots
from crop_images import get_images
# from yolo_optimized import run_yolov8_on_images
# from trial.crop_images import get_images
from yolov8_inference import run_yolov8_on_images

async def main():
    total_start_time = time.time()  # Start timing the total execution

    # Part 1: Capture screenshots asynchronously
    total_pages = 20  # Number of pages to capture screenshots from
    urls = generate_urls(total_pages)
    start_time = time.time()  # Start timing the screenshot capture
    await capture_multiple_screenshots(urls)
    end_time = time.time()  # End timing the screenshot capture
    print(f"Asynchronous execution took {end_time - start_time:.2f} seconds.")
    
    # Part 2: Crop images
    input_folder = "async_dataset"  # Folder where screenshots are saved
    output_folder = "dataset"  # Folder to save cropped images
    start_time = time.time()  # Start timing the image cropping
    get_images(input_folder, output_folder)
    end_time = time.time()  # End timing the image cropping
    print(f"Cropping execution time: {end_time - start_time:.2f} seconds")
    
    yolo_input_folder = "dataset"        
    yolo_output_folder = "final_output"  
    start_time = time.time()
    run_yolov8_on_images(yolo_input_folder, yolo_output_folder, batch_size=10, max_workers=4)
    end_time = time.time()
    print(f"YOLO Time Execution: {end_time - start_time:.2f} seconds")

    total_end_time = time.time()  # End timing the total execution
    total_execution_duration = total_end_time - total_start_time  # Calculate the total duration
    print(f"Total execution time: {total_execution_duration:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
