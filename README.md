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
