import asyncio
from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from rufus.web_scrape import scrape


class Retrieval:
    def __init__(self, api_token: str):
        self._vector_store = None

    @property
    def vector_store(self):
        return self._vector_store

    @vector_store.setter
    def vector_store(self, value):
        self._vector_store = value

    @staticmethod
    def chunk_text(
        text: str, chunk_size: int = 1500, chunk_overlap: int = 64
    ) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        return splitter.split_text(text)

    @staticmethod
    def extract_content(urls: List[str]) -> str:
        content = ""

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(scrape(urls))
        for result in results:
            content += result

        return content

    @staticmethod
    def get_embeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        normalize_embeddings=True,
        **kwargs
    ):
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=kwargs,
            encode_kwargs={"normalize_embeddings": normalize_embeddings},
        )

    def create_vector_store(self, chunks: List[str], embeddings: HuggingFaceEmbeddings):
        self.vector_store = FAISS.from_texts(chunks, embeddings)

    def create_chain(
        self, urls: List[str], chunk_size: int = 1500, chunk_overlap: int = 64
    ):
        content = self.extract_content(urls)
        self.create_vector_store(
            self.chunk_text(content, chunk_size, chunk_overlap),
            embeddings=self.get_embeddings(device="cpu"),
        )

    def scrape(self, instructions: str):
        information = dict()
        results = self.vector_store.similarity_search(instructions, k=7)

        for i, result in enumerate(results):
            information[f"Result {i}"] = result.page_content.replace('\n', ' ')

        print(information)

urls = ["https://www.joanneum.at/en/"]


retrieval = Retrieval(api_token="None")
content = retrieval.extract_content(urls)
retrieval.create_vector_store(
    retrieval.chunk_text(content, chunk_size=1500, chunk_overlap=64),
    embeddings=retrieval.get_embeddings(device="cpu"),
)

print(retrieval.scrape("What is the Mission ? "))
