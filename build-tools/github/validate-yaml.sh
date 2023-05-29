#!/bin/bash
set -eu
scriptdir=$(cd $(dirname $0) && pwd)
cd $scriptdir/../..

echo "------> Validating YAML"

# Validate adventure files against their schema
#
# We'll go into every directory that has a <xxx>.schema.json file,
# and validate all YAML files in that same directory against the schema file.
#
# The error messages produced by pajv are pretty bad, but we will just
# say that getting an error is better than getting NO error.
#
# If we ever care enough to do something about this, we should be interpreting
# the JSON error outputs of this tool and re-interpreting them with useful
# error messages.

# For magical and mysterious reasons, on GitHub actions using 'npx pajv validate' (which
# would normally be the way to run this command), hangs. It works fine on two of my machines,
# and also in an Ubuntu Docker container, and 'npx pajv help' works as well... but
# 'npx pajv validate' just hangs. Running the 'pajv' binary directly without the use of
# 'npx' does work... so we're just going to ¯\_(ツ)_/¯ and do that.

pajv=node_modules/.bin/pajv

all_schemas=$(find content -name \*.schema.json)

failures=false

for schema in $all_schemas; do
    dir=$(dirname $schema)
    echo "------> Validating $(basename $dir)"

    # Run pajv, remove all the lines that end in the word ' valid' -- those are not interesting
    # and just add noise.
    if ! $pajv validate --errors=text -s $schema -d "$dir/*.yaml" > validate.txt; then
        cat validate.txt | grep -vE ' valid$' || true
        failures=true
    fi
    rm validate.txt
done

# Also run the structure validator which compares en.yaml to the other languages
python tools/check-yaml-structure.py

if $failures; then
    exit 1
fi
