import os
from abc import abstractmethod

import pinecone

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENVIRONMENT")


class IR:
    @abstractmethod
    def search(self, query: str, k: int = 4):
        raise NotImplemented


class PineconeSearch(IR):
    def __init__(self, encoding_fnc) -> None:
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
        self.encoding_fnc = encoding_fnc

    def search(self, query: str, k: int = 4):
        q_embd = self.encoding_fnc.encode([query])[0]
        index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME"))

        result = index.query(
            vector=q_embd,
            top_k=k,
            include_metadata=True,
        )

        return [
            {"text": doc["metadata"]["text"], "metadata": doc["metadata"]}
            for doc in result["matches"]
        ]
