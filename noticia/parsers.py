import html
import re

CLEAN_HTML = re.compile('<.*?>')
REF_PAT = re.compile("Referências:.*?$")


def aosfatos_parser(text):
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


def newtral_parser(text):
    text = re.sub(r"\n\n", " ", text)
    text = re.sub(r"\| \d+\s+min lectura\s+", "", text)
    return text
