#!/bin/bash
set -e
pre-commit install
pybabel compile -f -d translations
cp -r /var/tmp/node_modules . 

if [[ -z "${BASE_URL}" ]]; then
  echo "export BASE_URL=\"https://${CODESPACE_NAME}-8080.preview.app.github.dev\"" >> ~/.bashrc
fi


