
# Content Retrieval and Vector Store Creation

This project demonstrates how to extract content from a specified URL, chunk the text into manageable pieces, create embeddings, and store them in a vector format for later retrieval. 

## Overview

The main functionality of this code is to:
1. Extract content from a list of URLs.
2. Chunk the extracted text into smaller segments for better processing.
3. Generate embeddings for the text chunks.
4. Create a vector store from the embeddings to facilitate efficient retrieval.
5. Query the vector store for specific information.

## Prerequisites

To run this code, you need to have the following:
- Python 3.x
- Required Python packages (see Installation section below)
- An API token for the Retrieval class if applicable (or replace `"None"` with a valid token)

## Installation

You can install the required packages using pip. Run the following command:

```bash
pip install -r requirements.txt
```


## Usage

1. **Set Up URLs:** Specify the URLs you want to scrape in the `urls` list.

    ```python
    urls = ["https://www.joanneum.at/en/"]
    ```

2. **Initialize the Retrieval Class:** Create an instance of the `Retrieval` class.

    ```python
    from rufus.retrival import Retrieval
    retrieval = Retrieval(api_token="None")
    ```

3. **Extract Content:** Use the `extract_content` method to get the content from the specified URLs.

    ```python
    content = retrieval.extract_content(urls)
    ```

4. **Create Vector Store:** Chunk the extracted content, generate embeddings, and create a vector store.

    ```python
    retrieval.create_vector_store(
        retrieval.chunk_text(content, chunk_size=1500, chunk_overlap=64),
        embeddings=retrieval.get_embeddings(device="cpu"),
    )
    ```

5. **Query the Vector Store:** Retrieve specific information by querying the vector store.

    ```python
    information = retrieval.scrape("What is the Mission ? ")
    ```

