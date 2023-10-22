#!/bin/bash
set -e

pushd "$(dirname "${BASH_SOURCE[0]}")/.."

# Make sure we are in the env.
source ./env/bin/activate

# Start the backend.
python3 src/main.py

popd
