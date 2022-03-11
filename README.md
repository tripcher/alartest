## Install
```shell
make isntall
```

## Start
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

## Create migration
```shell
export PYTHONPATH=.

python3 scripts/migrate.py revision --autogenerate -m "Comment"

python3 scripts/migrate.py upgrade head

```