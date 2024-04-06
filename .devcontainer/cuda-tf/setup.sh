# update pip
python -m pip install --upgrade pip

# install packages
pip install -e ".[dev]"

# install pre-commit hook if not installed already
pre-commit install
