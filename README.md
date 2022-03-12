## About
Используются подходы из HackSoft https://github.com/HackSoftware/Django-Styleguide

### Структура проекта:
auth - логика авторизации

users, roles - пользователи, пермишены и роли

sharding - вторая часть задания

health_chek - тестовый модуль для проверки, что разработка на правильном пути

### Структура приложений:
selectors - логика (в том числе бизнесовая) получения данных

services - основная бизнес логика приложения

dto - классический паттерн DTO, модели и схемы не используются так как слишком простой проект

api - http ручки

web - web странницы на шаблонах (фронт ОЧЕНЬ кривой)


## Getting started
1) Install: `make install`
2) Create database: 
```sql
create database alartest;
create user alartest with encrypted password 'alartest';
grant all privileges on database alartest to alartest;
```
3) Run migrations: 
```shell
export PYTHONPATH=.
python3 scripts/migrate.py upgrade head
```
4) Run server: `uvicorn app.main:app --reload`
5) Open: http://127.0.0.1:8000/login, http://127.0.0.1:8000/docs

## Install
```shell
make isntall
```

## Create database
```sql
create database alartest;
create user alartest with encrypted password 'alartest';
grant all privileges on database alartest to alartest;
```
For run tests:
```sql
alter user alartest createdb createrole;
```

## Create migration
```shell
export PYTHONPATH=.

python3 scripts/migrate.py revision --autogenerate -m "Comment"

python3 scripts/migrate.py upgrade head
```

## Run server
```shell
uvicorn app.main:app --reload 
```

## Login
* url: http://127.0.0.1:8000/login
* username: superuser
* password: superuser

## Lint
```shell
make lint
```

## Test
```shell
make test
```