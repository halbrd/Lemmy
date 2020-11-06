# Lemmy

Your friendly neighbourhood Discord bot

## Install requirements

```
pipenv install
```

## Configure

```bash
cp config/lemmy.example.ini config/lemmy.ini
cp config/contexts.example.ini config/contexts.ini
# edit lemmy.ini and contexts.ini as required
```

## Run

```
python main.py
```

### Run with Docker

```
docker build . -t lemmy
docker run lemmy
```
