
# [DiceDB](https://github.com/dicedb/cli) CLI with Auto Completion and Syntax Highlighting


## Running with Poetry

1. Install [Poetry](https://python-poetry.org/docs/#installation):

   ```bash
   $ curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Run the project using Poetry:

   ```bash
   $ poetry install
   $ poetry shell
   $ dice

   Examples | Alternates :
      - dice
      - dice -d dsn
      - dice -h 127.0.0.1 -p 6379
      - dice -h 127.0.0.1 -p 6379 -a <password>
      - dice --url redis://localhost:7890/3

   ```

## Running with a Virtual Environment
```bash
$ python -m venv venv
$ . venv/bin/activate
$ pip install -e .
$ chmod +x main.py
$ ./main

Examples | Alternates :
      - ./main
      - ./main -d dsn
      - ./main -h 127.0.0.1 -p 6379
      - ./main -h 127.0.0.1 -p 6379 -a <password>
      - ./main --url redis://localhost:7890/3
```

## Release Procedure

```bash
$ pip install bumpversion
$ bumpversion patch/minor/major
```
