import os

import openai
import pinecone
from loguru import logger


EMBEDDING_MODEL = "text-embedding-ada-002"


def pinecone_index(api_key=None, environment=None, index=None):
    api_key = api_key or os.environ["PINECONE_API_KEY"]
    environment = environment or os.environ["PINECONE_ENVIRONMENT"]
    index = index or os.environ["PINECONE_INDEX_NAME"]
    pinecone.init(api_key=api_key, environment=environment)
    return pinecone.Index(index)


def pinecone_batch_insert(data):
    index = pinecone_index()
    to_insert = []

    batch_size = 32
    for i in range(0, len(data), batch_size):
        rows = data[i:i + batch_size]
        logger.info(f"Inserting {len(rows)} rows on vector db...")
        ids = [f"{index}-{r.metadata['hash']}" for index, r in enumerate(rows)]
        response = openai.Embedding.create(
            input=[r.page_content for r in rows],
            engine=EMBEDDING_MODEL
        )
        embedings = [record['embedding'] for record in response["data"]]
        meta = [{"text": r.page_content, "url": r.metadata["url"]} for r in rows]
        to_insert = list(zip(ids, embedings, meta))
        index.upsert(vectors=to_insert)
        logger.info(f"Total of {len(to_insert)} rows inserted")

    return to_insert
