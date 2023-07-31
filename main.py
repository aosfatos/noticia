import os
from hashlib import md5

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

from core.google import search
from core.entries import download


resp = search(os.environ["GOOGLE_API_KEY"], max_days=3, publisher="newtral.es")


def load_docs(data):
    sources = []
    for row in data:
        content = download(row["claimReview"][0]["url"])
        _hash = md5(row["claimReview"][0]["title"].encode()).hexdigest()
        sources.append(
            Document(
                page_content=content,
                metadata={"url": row["claimReview"][0]["url"], "hash": _hash}
            )
        )

    splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    documents = splitter.split_documents(sources)
    return documents


docs = load_docs(resp)
