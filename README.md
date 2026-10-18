# pyiem
Iowa Electronic Markets

## Setup
```zsh
conda env create -f environment.yaml
conda activate pyiem
pre-commit install
```

and
```shell
pip install -e ".[dev,plot,test]"
```

## Configuration
- `conf/markets.json` lists the markets, bundles and assets.
- Copy `conf/login_example.json` to `conf/login.json` and fill in your IEM login. `conf/` is
  git-ignored apart from those two files.

## Tests
```shell
pytest
```
