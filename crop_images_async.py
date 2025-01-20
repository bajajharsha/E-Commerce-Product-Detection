import cv2
import os
import asyncio
import aiofiles
from pathlib import Path
import time

async def crop_image_async(image_path, output_folder, num_parts=8):
    """
    Asynchronously crops an image into smaller parts and saves them.
    """
    try:
        img = cv2.imread(image_path)  # Read the image
        img_height, img_width, _ = img.shape  # Get the image dimensions
        part_height = img_height // num_parts  # Calculate the height of each part
        base_filename = Path(image_path).stem  # Get the base filename without extension

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Crop the image into smaller parts
        tasks = []
        for i in range(num_parts):
            y_start = i * part_height
            y_end = (i + 1) * part_height if i != num_parts - 1 else img_height
            cropped_img = img[y_start:y_end, 0:img_width]  # Crop the image

            # Save each cropped image asynchronously
            cropped_image_path = os.path.join(output_folder, f"{base_filename}_part_{i+1}.png")
            tasks.append(save_image_async(cropped_image_path, cropped_img))

        await asyncio.gather(*tasks)  # Process all save tasks concurrently
        # print(f"Cropping completed for {image_path}. Cropped images are saved in '{output_folder}'.")

    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

async def save_image_async(output_path, image):
    """
    Asynchronously saves an image to disk using aiofiles.
    """
    try:
        is_success, buffer = cv2.imencode(".png", image)  # Encode image to memory buffer
        if not is_success:
            raise ValueError(f"Failed to encode image for {output_path}")

        async with aiofiles.open(output_path, mode="wb") as f:
            await f.write(buffer.tobytes())  # Write buffer to file asynchronously
    except Exception as e:
        print(f"Error saving image {output_path}: {e}")

async def process_images(input_folder, output_folder):
    """
    Processes all images in the input folder concurrently.
    """
    tasks = []
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            tasks.append(crop_image_async(file_path, output_folder))

    await asyncio.gather(*tasks)  # Process all images concurrently

# if __name__ == "__main__":
#     input_folder = "async_dataset"
#     output_folder = "cropped_output"
#     start_time = time.time()
#     asyncio.run(process_images(input_folder, output_folder))
#     end_time = time.time()
#     print(f"Total processing time: {end_time - start_time:.2f} seconds")
