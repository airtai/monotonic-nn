# install Python packages in virtual environment
# python3.11 -m venv .venv-3.11
# source .venv-3.11/bin/activate
# python -m pip install --upgrade pip

# needed to make sure default python is 3.9 instead of 3.11
sudo ln -s -f /usr/local/bin/python3.9 /usr/bin/python3

# install packages and make sure we use TF 2.14.1
pip install -e .[dev] tensorflow==2.14.1

# install pre-commit hook if not installed already
pre-commit install
