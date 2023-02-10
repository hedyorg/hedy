#!/bin/bash
set -e
pre-commit install
pybabel compile -f -d translations
cp -r /var/tmp/node_modules . 
echo "export BASE_URL=\"https://${CODESPACE_NAME}-8080.preview.app.github.dev\"" >> ~/.bashrc