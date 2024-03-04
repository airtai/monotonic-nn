# install Python packages in virtual environment
# python3.11 -m venv .venv-3.11
# source .venv-3.11/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
