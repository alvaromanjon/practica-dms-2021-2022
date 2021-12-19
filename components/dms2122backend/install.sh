#!/bin/bash

TEMP_DIR="$(mktemp -d)"

# Install
cp -R * "${TEMP_DIR}"
pushd "${TEMP_DIR}"
./setup.py install
popd

rm -R "${TEMP_DIR}"

dms2122backend-create-database-of-questions
