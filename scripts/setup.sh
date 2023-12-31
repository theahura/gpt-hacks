#!/bin/bash
set -e

pushd "$(dirname "${BASH_SOURCE[0]}")/.."

# Set up the python env.
if ! command -v python3.11 --version &> /dev/null; then
  echo "Setting up python"
  sudo apt -y install wget build-essential libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev \
    zlib1g-dev
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt -y install python3.11 python3.11-dev python3.11-venv
  python3.11 -m venv env
fi

# Checks if env exists. If it doesnt, creates it.
if [ ! -d "./env" ]; then
  echo "Creating venv."
  python3.11 -m venv env
fi

# Installs requirements.
echo "Installing requirements."
source env/bin/activate
pip install -r requirements.txt

# Sets up env. Queries the user for an OPENAI_API_KEY token, and writes it to
# the .env file.

# For macOS, .env files are not read and must be set by export and source .env

echo "Setting up env."
touch .env
echo "Please provide your OPENAI_API_KEY:"
read OPENAI_API_KEY
echo "OPENAI_API_KEY=$OPENAI_API_KEY" > .env

popd
