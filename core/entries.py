import html
import re
from hashlib import md5

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from newspaper import Article


CLEAN_HTML = re.compile('<.*?>')
REF_PAT = re.compile("Referências:.*?$")


def clean_text(text):
    text = re.sub(
        r'(</?p>|\s+\(<a href=".*?"\s+target="_blank">veja aqui</a>\))',
        "",
        text,
    )
    text = re.sub(r'(\r|\n)', ' ', text)
    text = re.sub(CLEAN_HTML, "", text)
    text = re.sub(r"\s+", " ", text)
    if has_refs := REF_PAT.search(text):
        span = has_refs.span()
        text = text[:span[0]].strip()
    return html.unescape(text)


def download(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text


def prepare_documents(data):
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
