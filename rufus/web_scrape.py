import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def extract_html_from_url(url):
    try:
        # Fetch HTML content from the URL using aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
                content = (
                    await response.text()
                )  # Get the response content asynchronously

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")

        # Extract only <p> tags and their content, remove all other tags
        paragraphs = soup.find_all("p")  # Get all paragraph tags
        text_content = ""

        for paragraph in paragraphs:
            text_content += (
                paragraph.get_text() + "\n"
            )  # Append the text of each paragraph

        return text_content

    except aiohttp.ClientError as e:
        print(f"Error fetching data from {url}: {e}")
        return f"Error fetching data from {url}: {e}"


async def fetch_multiple_urls(urls):
    # Use asyncio.gather to run multiple tasks concurrently
    tasks = [extract_html_from_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


async def main():
    results = await fetch_multiple_urls(
        ["https://lilianweng.github.io/posts/2023-06-23-agent/"]
    )

    return results

# results = asyncio.run(main())
# for result in results:
#     print(result)
