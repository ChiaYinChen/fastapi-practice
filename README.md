# FastAPI practice

Build a basic RESTFul API using FastAPI, including interactive API documentation.

## Installation

Install requirements

```
$ pip install -r requirements/prod.txt
```

Install requirements for developing packages

```
$ pip install -r requirements/dev.txt
```

## Docker

Deploy

```
$ docker-compose up -d --build
```

Down

```
$ docker-compose down --rmi local
```

## Running the tests

```
$ tox
```

## Interactive API docs

[http://127.0.0.1:8008/docs](http://127.0.0.1:8008/docs)
