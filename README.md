# NoticIA

## Run the project locally

```shell
cp env.example .env

docker-compose -f compose.yml up
```

## Schedule claim review download task

```shell
crontab -r

0 0 * * * python main.py
```
