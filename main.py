import os

from loguru import logger

from core.entries import prepare_documents
from core.google import search
from core.vectordb import pinecone_batch_insert


publishers = ["aosfatos.org", "newtral.es"]
max_days = 3
for publisher in publishers:
    logger.info(f"Download claim review data from {publisher}...")
    response = search(os.environ["GOOGLE_API_KEY"], max_days=max_days, publisher=publisher)
    logger.info("Done!")
    documents = prepare_documents(response)
    logger.info("Inserting data on vector db")
    inserted = pinecone_batch_insert(documents)
    logger.info("Done!")
