FROM python:3.11-alpine

ENV LIBRD_VER=2.6.1

WORKDIR /cli-tool

RUN apk add --no-cache --virtual .make-deps bash make wget git gcc g++ && apk add --no-cache musl-dev zlib-dev openssl zstd-dev pkgconfig libc-dev

RUN wget https://github.com/edenhill/librdkafka/archive/v${LIBRD_VER}.tar.gz
RUN tar -xvf v${LIBRD_VER}.tar.gz && cd librdkafka-${LIBRD_VER} && ./configure --prefix /usr && make && make install && make clean

RUN pip install --upgrade pip

RUN apk update && apk upgrade

RUN pip install --upgrade pip setuptools wheel

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./source/cli-tool /cli-tool

COPY ./pyproject.toml /cli-tool

RUN poetry install --no-interaction --only cli-tool

RUN poetry update

ENV PYTHONPATH=/cli-tool
ENTRYPOINT ["python", "-u", "main.py"]
