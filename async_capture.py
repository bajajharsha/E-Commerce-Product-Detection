import asyncio
import time
from playwright.async_api import async_playwright

# Generate URLs dynamically based on the number of pages
def generate_urls(total_pages):
    '''
    urls = [
        'https://www.flipkart.com/search?q=laptops',
        'https://www.flipkart.com/search?q=smartphones',
        'https://www.flipkart.com/search?q=washing+machine',
        'https://www.flipkart.com/search?q=refridgerator',
        'https://www.flipkart.com/search?q=monitors',
        'https://www.flipkart.com/search?q=cameras',
        'https://www.flipkart.com/search?q=Tv',
        'https://www.flipkart.com/search?q=gaming+console',
        'https://www.flipkart.com/search?q=speakers',
        'https://www.flipkart.com/search?q=earbuds',
        'https://www.flipkart.com/search?q=monitors',
        'https://www.flipkart.com/search?q=printers',
        'https://www.flipkart.com/search?q=microwave',
        'https://www.flipkart.com/search?q=blender',
        'https://www.flipkart.com/search?q=analog+watches',
        'https://www.flipkart.com/search?q=mouse',
        'https://www.flipkart.com/search?q=headphones',
        'https://www.flipkart.com/search?q=vaccum+cleaner',
        'https://www.flipkart.com/search?q=drone',
        'https://www.flipkart.com/search?q=rc+helicopter',
        'https://www.flipkart.com/search?q=action+figures',
        'https://www.flipkart.com/search?q=air+purifier',
        'https://www.flipkart.com/search?q=tablets',
        'https://www.flipkart.com/search?q=yonex',
        'https://www.flipkart.com/search?q=remote%20control%20car',
        'https://www.flipkart.com/search?q=dyson',
        'https://www.flipkart.com/search?q=kookaburra+bat',
        'https://www.flipkart.com/search?q=badminton+racquet',
    ]
    '''
    urls = [f"https://www.amazon.in/s?k=mobile&page={page}&crid=2CTVST35VBTUF&qid=1737113307&sprefix=,aps,179&xpid=ksZe5iHU6Giqs" for page in range(1, total_pages + 1)]
    return urls

# Capture a screenshot asynchronously for a given URL
async def capture_screenshot_async(browser, url, save_path):
    try:
        page = await browser.new_page()  # Reusing the browser instance
        await page.goto(url)  # Navigate to the URL with a timeout
        await page.screenshot(path=save_path, full_page=True)  # Capture full-page screenshot
        await page.close()  # Close the page after taking the screenshot
        # print(f"Screenshot saved to {save_path}")
    except Exception as e:
        print(f"Error capturing screenshot for {url}: {e}")

# Capture multiple screenshots concurrently with error handling
async def capture_multiple_screenshots(urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Launch browser once

        tasks = [
            capture_screenshot_async(browser, url, f"async_dataset/screenshot_{i+1}.png")
            for i, url in enumerate(urls)
        ]
        
        # Gather all tasks and handle exceptions
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result, url in zip(results, urls):
            if isinstance(result, Exception):
                print(f"Error processing URL {url}: {result}")

        await browser.close()  # Close the browser after all screenshots are taken

# if __name__ == "__main__":
#     total_start_time = time.time()  # Start timing the total execution

#     # Part 1: Capture screenshots asynchronously
#     total_pages = 20  # Number of pages to capture screenshots from
#     urls = generate_urls(total_pages)
    
#     start_time = time.time()  # Start timing the screenshot capture
#     asyncio.run(capture_multiple_screenshots(urls))
#     end_time = time.time()  # End timing the screenshot capture
#     print(f"Asynchronous execution took {end_time - start_time:.2f} seconds.")
