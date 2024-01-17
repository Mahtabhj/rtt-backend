#!/bin/bash

celery -A rtt worker -l INFO -Q queue-stag,queue-es-stag