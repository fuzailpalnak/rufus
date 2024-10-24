import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from loguru import logger

# A set to track visited URLs to prevent circular links
visited_urls = set()


async def extract_html_from_url(url):
    if url in visited_urls:
        return ""  # Skip already visited URLs to prevent loops

    visited_urls.add(url)

    try:
        logger.info(f"Extracting {url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                content_type = response.headers.get("Content-Type", "")
                encoding = "utf-8"  # Default encoding

                if "charset=" in content_type:
                    encoding = content_type.split("charset=")[-1]

                content = await response.text(encoding=encoding)

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")

        # Extract only <p> tags and their content
        paragraphs = soup.find_all("p")  # Get all paragraph tags
        text_content = ""

        for paragraph in paragraphs:
            text_content += paragraph.get_text() + "\n"

        list_items = soup.find_all("li")  # Get all list items
        for li in list_items:
            link = li.find("a", href=True)  # Find the first <a> tag within the <li>
            if link:
                nested_url = urljoin(url, link["href"])  # Resolve relative URLs
                # Fetch content from the nested URL, but do not go deeper
                nested_text_content = await extract_nested_content(nested_url)
                if nested_text_content is not None:
                    text_content = text_content + nested_text_content

        return text_content

    except aiohttp.ClientError as e:
        logger.error(f"Error fetching data from {url}: {e} for url {url}")
    except UnicodeDecodeError as e:
        logger.error(f"Unicode decode error: {e} for url {url}")


async def extract_nested_content(url):
    """Fetch content from the nested URL but do not go deeper."""
    if url in visited_urls:
        return ""  # Skip already visited URLs to prevent loops

    visited_urls.add(url)  # Mark the nested URL as visited

    try:
        logger.info(f"Extracting Nested Url {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                content = await response.text()

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")

        paragraphs = soup.find_all("p")
        nested_content = ""

        for paragraph in paragraphs:
            nested_content += paragraph.get_text() + "\n"
        return nested_content

    except aiohttp.ClientError as e:
        logger.error(f"Error fetching data from {url}: {e} for url {url}")
    except UnicodeDecodeError as e:
        logger.error(f"Unicode decode error: {e} for url {url}")


async def fetch_multiple_urls(urls):
    # Use asyncio.gather to run multiple tasks concurrently
    tasks = [extract_html_from_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


async def main():
    # Reset visited URLs before starting the main function
    global visited_urls
    visited_urls = set()

    results = await fetch_multiple_urls(
        [
            "https://www.tugraz.at/en/studying-and-teaching/degree-and-certificate-programmes/masters-degree-programmes/computer-science"
        ]
    )

    return results


# Uncomment below to run the script and print the results
loop = asyncio.get_event_loop()
if loop.is_running():
    # Handle the case where the loop is already running (e.g., in Jupyter)
    tasks = [main()]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    for result in results:
        print(result)
else:
    results = loop.run_until_complete(main())
    for result in results:
        print(result)
