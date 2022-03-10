
## Install
```shell
make isntall
```

## Install dev
```shell
make isntall-dev
```

## Lint
```shell
make lint
```

## Create migration
```shell
alembic revision --autogenerate -m "Comment"

alembic upgrade head
```