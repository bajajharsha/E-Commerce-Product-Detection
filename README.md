# Problem Statement

### E-Commerce Product Detection and Analysis

Design a system to capture and analyze screenshots from an e-commerce website, focusing on the automated identification and classification of key visual elements such as product price, primary product image, product description, and product rating. The system should programmatically capture screenshots and use image processing techniques to segment and classify these components into distinct categories with minimal overlap or errors. It should support a maximum of 3-4 clearly defined classes and be adaptable to varying e-commerce layouts with minimal manual intervention.

To ensure robustness and scalability, the system will incorporate:

- **Error Handling:** Try-except blocks, custom exceptions, and best practices for structured error management.
- **Typing and Validation:** Type hints (`typing` module) and Pydantic for structured data validation.
- **Memory Management:** Python's memory model, garbage collection, and GIL considerations.
- **Concurrency:** Threading, event loops, coroutines, and `asyncio` for efficient multitasking.

These principles will ensure the system is efficient, maintainable, and capable of handling diverse e-commerce platforms effectively.

# My Findings

- Web scraping is I/O bound task - The major delay comes from **waiting** for the server to respond (network latency) and CPU is not used. Waiting for external resources
- Image processing - CPU-Bound Task. Heavy computation (e.g., image classification, feature extraction).
- 

# Sub-Tasks

## 1.  Data Collection (Screenshot Capture)

- Capture screenshots of product pages programmatically.
- Save images with unique identifiers and error handling for invalid URLs or capture failures.

### Topics to Apply:

- **Error Handling Basics:** Use `try-except` blocks to manage web automation issues like `TimeoutError`.
- **Custom Exceptions:** Create exceptions like `InvalidURLException` for handling incorrect URLs.
- **Raising Exceptions:** Use `raise` statements for critical errors during screenshot capture.

## 2.  Image Segmentation and Preprocessing

- Segment the image into regions of interest (price, image, description, rating).

### Topics to Apply:

- **Typing Module:** Use type hints for image data types (`np.ndarray`) and segmentation results.
- **Error Handling:** Implement error handling for invalid image formats and missing regions.
- **Memory Management:** Optimize image loading and storage by working with compressed formats when possible

## 3.  Feature Extraction and Classification

- Apply object detection models (YOLO/OpenCV DNN) for extracting key elements.
- Classify and label the extracted regions into product price, image, description, and rating.
- Validate extracted data (e.g., check if price is numeric, rating within 1-5).

### Topics to Apply:

- **Typing & Validation:** Use Pydantic models to validate extracted data types (price as `float`, rating as `int`).
- **Error Handling:** Raise exceptions for invalid extracted data (e.g., `InvalidPriceError`)

# Execution

## 1. Screenshot

- Tested the [screenshot one API](https://screenshotone.com/) but found it takes 40 seconds to process a single request
- Compared performance between threading and asyncio implementations
- Asyncio showed slight performance improvements, though the difference was minimal for 10 URLs
- Asyncio performs better because it uses event loops to handle tasks concurrently. Since it runs on a single main thread, it reduces system overhead
- In contrast, threading creates multiple concurrent threads, which increases system overhead and reduces overall efficiency

Problems/Edge cases

1. When using gather in asyncio, if one task fails or causes an exception, all other awaitable are cancelled
    
    **Fix:**
    
    - return_exceptions=True
    - asyncio.as_complete
    - **Handle Exceptions Within coroutines -** handle their own exceptions so that they do not propagate beyond the task themselves.
    - **Handle Exceptions From asyncio.gather() -** wrap the call to asyncio.gather() in a try-except block.
    - Links: [StackOverflow](https://stackoverflow.com/questions/54987361/python-asyncio-handling-exceptions-in-gather-documentation-unclear), [Super fast python](https://superfastpython.com/asyncio-gather-exception/)

## 2. YOLO

- Used the pre-trained YOLO model for object detection.
- Initially processed images one at a time, which proved time-consuming.
- While batch processing would be faster, it requires significant computational resources.
- To balance speed and resources, I'll implement a process pool.

Problems faced

1. ModuleNotFoundError: No module named '_lzma'
    
    **Fix:** You may be missing the `xz` libraries ([Gist](https://gist.github.com/iandanforth/f3ac42b0963bcbfdf56bb446e9f40a33))
    

## 3. Segmentation

- segmenting on the basis of classes
- using the box cordinates and classes to segment

# Optimizations Scope:

1. **Minimize Disk I/O**
    - Use in-memory objects (e.g., `BytesIO`) to pass image data between steps without repeatedly saving and loading files.
2. **Use `concurrent.futures.ProcessPoolExecutor` for YOLO**:
    - Parallelize YOLO inference across CPU cores for faster execution.
    - Avoid holding unnecessary objects in memory to save resources.
3. **Optimize Cropping with `asyncio`**:
    - As cropping is typically I/O-bound (loading and saving images), asynchronous file handling can speed it up.
4. **Efficient Memory Usage in Segmentation**:
    - Avoid saving intermediate results unnecessarily.
    - Directly process and pass objects in memory, reducing disk I/O.
5. **Enable Concurrent Browser Contexts or Pages**
- Playwright supports creating multiple browser contexts or pages, which can run in parallel. This approach can significantly reduce the time spent capturing screenshots.
