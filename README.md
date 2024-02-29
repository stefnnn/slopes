# Slopes

Get on your skis, mountaineer!

## Getting Started

Install the dependencies with poetry:

```bash
poetry install
```

Spin up a database (or configure one in .env) and sync your schema:

```bash
docker-compose up -d
poetry createdb
```

Then start your server:

```bash
poetry run runserver
```
