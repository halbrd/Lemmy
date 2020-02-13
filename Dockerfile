FROM python:3-alpine

RUN apk add --no-cache imagemagick
RUN apk add --no-cache imagemagick-dev
RUN apk add --no-cache git
RUN apk add --no-cache gcc
RUN apk add --no-cache musl-dev
RUN pip install pipenv

WORKDIR /app
COPY . .

RUN pipenv install

CMD pipenv run python lemmy.py
