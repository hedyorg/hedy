#!/bin/bash
set -eu
if [[ "$HEROKU_APP_NAME" != "hedy-test" ]]; then
    # On the non-test instances, run nginx+Flask with the nginx config
    # to forward to the other instance.
    echo "Normal instance, A/B testing startup."
    bin/start-nginx-debug gunicorn -c config/gunicorn.conf.py app:app
else
    # On the test instance, just run Flask
    echo "Test instance, plain startup."
    gunicorn app:app
fi
