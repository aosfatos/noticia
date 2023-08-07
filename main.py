import os
from collections import namedtuple

from loguru import logger

from noticia.google import search
from noticia.news import prepare_documents
from noticia.parsers import aosfatos_parser, newtral_parser
from noticia.vectordb import pinecone_batch_insert

Publisher = namedtuple("Publisher", ["url", "parser"])


publishers = [
    Publisher("aosfatos.org", aosfatos_parser),
    Publisher("newtral.es", newtral_parser),
]
max_days = 1
for publisher in publishers:
    logger.info(f"Download claim review data from {publisher}...")
    response = search(
        os.environ["GOOGLE_API_KEY"], max_days=max_days, publisher=publisher.url
    )
    logger.info("Done!")
    documents = prepare_documents(response, publisher.parser)
    logger.info("Inserting data on vector db")
    inserted = pinecone_batch_insert(documents)
    logger.info("Done!")
