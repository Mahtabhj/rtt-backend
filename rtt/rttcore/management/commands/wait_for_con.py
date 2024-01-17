import subprocess
import time
from django.db import connections
from django.core.management.base import BaseCommand
from elasticsearch_dsl.connections import connections


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for db...')
        db_time = 0
        while db_time < 10:
            try:
                conn = connections.get_connection()
                if conn:
                    self.stdout.write('DB Connection stable')
                    break
                break
            except IOError:
                time.sleep(1)
                print("DB is not stable yet!")
            db_time += 1
        self.stdout.write('Waiting for elasticsearch...')
        time.sleep(60)
        es_conn = None
        time_count = 0
        while not es_conn:
            try:
                time_count += 1
                if time_count > 10:
                    es_conn = True
                    break
                self.stdout.write('Running for elasticsearch Build...')
                p = subprocess.call(['sh', './rebuild.sh'])
                if p == 0:
                    es_conn = True
                    break
                else:
                    es_conn = None
                    raise Exception
            except Exception as e:
                self.stdout.write('Elasticsearch unavailable, waiting 1 second {}'.format(str(e)))
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Elasticsearch available!'))
