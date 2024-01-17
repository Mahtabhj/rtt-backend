#!/bin/bash

#python manage.py wait_for_celery
celery -A rtt worker -l INFO -Q queue-prod,queue-es-prod