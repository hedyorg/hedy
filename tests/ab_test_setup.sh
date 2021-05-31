#!/bin/bash
# Run the server in an A/B testing setup.
scriptdir=$(cd $(dirname $0) && pwd)
cd $scriptdir/..
PIDS=""
trap 'kill $PIDS; exit' INT

env FLASK_ENV=development IS_TEST_ENV=true PORT=5050 HEROKU_APP_NAME=localhost SECRET_KEY=TheSecret python3 app.py &
PIDS="$PIDS $!"

env FLASK_ENV=development PROXY_TO_TEST_HOST=http://localhost:5050 PROXY_TO_TEST_PROPORTION=100 SECRET_KEY=TheSecret HEROKU_APP_NAME=localhost python3 app.py &
PIDS="$PIDS $!"

echo 'Run the following command:'
echo ''
echo '======================================================================'
echo ''
echo "    curl -H 'X-Testing: 1' -vv http://localhost:5000/session_test"
echo ''
echo '======================================================================'
echo ''

wait
