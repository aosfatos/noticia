# NoticIA

## Run the project locally

```shell
cp env.example .env

docker-compose -f compose.yml up
```

## Schedule claim review download task

Execute everyday 1am UTC

```shell
crontab -e

0 1 * * * python main.py
```


## Querying Pinecone vector DB

```python
import openai
import pinecone

pinecone.init(api_key=api_key, environment=environment)
index = pinecone.Index("noticia")

query = "query"
vector = openai.Embedding.create(input=query, model="text-embedding-ada-002")
search_result = index.query(
    top_k=2,
    vector=vector["data"][0]["embedding"],
    include_metadata=True
)
```
