from abc import abstractmethod

import openai


class Embedding:
    def __init__(self, model_name):
        self.model_name = model_name

    @abstractmethod
    def encode(self, texts):
        raise NotImplementedError


class OpenAIEmbedding(Embedding):
    def __init__(self, model_name="text-embedding-ada-002"):
        self.model_name = model_name

    def encode(self, texts):
        texts = [text.replace("\n", " ") for text in texts]

        response = openai.Embedding.create(input=texts, model=self.model_name)
        embeddings = [embedding["embedding"] for embedding in response["data"]]
        return embeddings
