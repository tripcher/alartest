
## Install
```shell
make isntall
```

## Start
```shell
uvicorn app.main:app --reload 
```

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