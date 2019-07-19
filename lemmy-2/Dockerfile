FROM python:3-alpine

RUN apk add --no-cache imagemagick
RUN apk add --no-cache imagemagick-dev
RUN apk add --no-cache git
RUN apk add --no-cache gcc
RUN apk add --no-cache musl-dev

WORKDIR /app
COPY . .

RUN pip install --user -r requirements.txt

CMD python lemmy.py
