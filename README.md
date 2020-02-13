# Lemmy

Your friendly neighbourhood Discord bot

## Install requirements

```
pipenv install
```

## Configure

```bash
cp config.example.json config.json
# edit config.json
```

The config attributes `token` and `default_manifest` are mandatory.

## Run

```
python main.py
```

### Run with Docker

```
docker build . -t lemmy
docker run lemmy
```
