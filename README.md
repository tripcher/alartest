## About
Uses paradigms from  HackSoft guid https://github.com/HackSoftware/Django-Styleguide

##Run
* install
* create database
* create migration
* run server

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