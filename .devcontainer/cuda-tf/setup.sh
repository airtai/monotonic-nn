# update system
apt update
apt upgrade -y

# install Linux tools and Python 3 libs
apt install -y software-properties-common python3-dev python3-pip python3-wheel python3-setuptools

# install Python packages
# python3 -m pip install --upgrade pip
# pip3 install -r .devcontainer/requirements.txt --user --extra-index-url https://pypi.nvidia.com

# update pip
python -m pip install --upgrade pip

# install packages
pip install -e ".[dev]" --user --extra-index-url https://pypi.nvidia.com

# install pre-commit hook if not installed already
pre-commit install
