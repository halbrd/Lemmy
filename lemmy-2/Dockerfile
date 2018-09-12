FROM python:3-alpine

RUN apk add imagemagick
RUN apk add git
RUN apk add gcc
RUN apk add musl-dev

WORKDIR /app
COPY . .

RUN pip install --user -r requirements.txt

CMD python lemmy.py