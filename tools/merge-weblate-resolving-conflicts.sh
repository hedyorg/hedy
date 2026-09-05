#!/bin/bash
# This script will check out the Weblate repository, and automatically merge
# it with `main` resolving conflicts.
set -eu
set -x

# Checkout Weblate main repo
git remote add weblate-main https://hosted.weblate.org/git/hedy/adventures/ || true
git fetch weblate-main
git checkout -B weblate-hedy-adventures-conflicts weblate-main/main

# Normalize files in Weblate main repo
doit run _autopr _autopr_weblate
git commit -am 'Normalize Weblate branch' --allow-empty

# Merge from origin, preferring Weblate's changes
git fetch origin
git merge -s recursive -X ours origin/main --no-edit
