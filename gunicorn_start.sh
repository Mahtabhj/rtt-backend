#!/bin/bash

echo "Running Migrate ...."
python manage.py migrate
python manage.py migrate rttauth
python manage.py migrate rttdocument
python manage.py migrate rttnews
python manage.py migrate rttregulation
python manage.py migrate rttproduct
python manage.py migrate rttorganization

echo "Checking Elasticsearch rebuild ...."
es_rebuild=${1:-false}
if $es_rebuild; then
  echo "Proceed Elasticsearch rebuild ...."
  python manage.py wait_for_con
else
  echo "Elasticsearch rebuild skipped!"
fi

echo "Running Collect Static..."
python manage.py collectstatic --no-input

echo "Running Gunicorn..."
exec gunicorn rtt.wsgi --name rtt --workers 4 --timeout 240 -b 0.0.0.0:8000
