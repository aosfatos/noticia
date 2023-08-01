import os
from collections import namedtuple

from loguru import logger

from core.google import search
from core.news import prepare_documents
from core.parsers import aosfatos_parser, newtral_parser
from core.vectordb import pinecone_batch_insert


Publisher = namedtuple("Publisher", ["url", "parser"])


publishers = [
    Publisher("aosfatos.org", aosfatos_parser),
    Publisher("newtral.es", newtral_parser),
]
max_days = 2
for publisher in publishers:
    logger.info(f"Download claim review data from {publisher}...")
    response = search(os.environ["GOOGLE_API_KEY"], max_days=max_days, publisher=publisher.url)
    logger.info("Done!")
    documents = prepare_documents(response, publisher.parser)
    logger.info("Inserting data on vector db")
    inserted = pinecone_batch_insert(documents)
    logger.info("Done!")
