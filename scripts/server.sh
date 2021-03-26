#!/bin/bash
ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

#waiting for db
# ./scripts/wait-for-it.sh $DB_HOST:$DB_PORT


# python manage.py collectstatic --noinput
python manage.py migrate

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn config.wsgi:application \
    --worker-class gevent \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --timeout 3000
    --access-logfile=-
    --error-logfile=-

# python manage.py runserver 0.0.0.0:8000
