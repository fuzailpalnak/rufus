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
        self._embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

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

    def create_retriever(self, chunks: List[str]) -> FAISS:
        faiss_store = FAISS.from_texts(chunks, self._embeddings)
        return faiss_store

    def create_chain(
        self, urls: List[str], chunk_size: int = 1500, chunk_overlap: int = 64
    ):
        content = self.extract_content(urls)
        vector_store = self.create_retriever(
            self.chunk_text(content, chunk_size, chunk_overlap)
        )

        print(vector_store.similarity_search("What are the Focus areas ?", k=7))
        # self.rag = RetrievalQA.from_chain_type(
        #     llm=self._llm,
        #     chain_type="stuff",
        #     retriever=content_retriever,
        #     return_source_documents=True
        # )

    # def scrape(self, instructions: str):
    #     return self.rag.run(instructions)


retrival = Retrieval(api_token="None")
retrival.create_chain(
    [
        "https://www.tugraz.at/en/studying-and-teaching/degree-and-certificate-programmes/masters-degree-programmes/computer-science"
    ]
)

# print(retrival.scrape("What are the Focus areas ?"))
