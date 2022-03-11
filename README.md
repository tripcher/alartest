
## Install
```shell
make isntall
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