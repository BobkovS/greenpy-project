#!/bin/sh
exec gunicorn -b :8080 --workers $SERVER_WORKERS --threads $SERVER_THREADS --worker-class=gevent --limit-request-line $LIMIT_REQUEST_LINE --limit-request-field_size $LIMIT_REQUEST_FIELD_SIZE --timeout $SERVER_TIMEOUT --access-logfile - --error-logfile - --log-level=info greenpy:app
