import html
import re

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
