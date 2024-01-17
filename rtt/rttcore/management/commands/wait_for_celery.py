import subprocess
import time
from django.core.management.base import BaseCommand
from rtt.settings import SERVER_STATE

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for celery...')
        celery_conn = None
        time_count = 0
        while not celery_conn:
            try:
                time_count += 1
                if time_count > 5:
                    celery_conn = True
                    break
                self.stdout.write('Running for Celery Start...')
                p = subprocess.call(['sh', './celery_start_{}.sh'.format(SERVER_STATE)])
                if p == 0:
                    self.stdout.write(self.style.SUCCESS('Celery available!'))
                    celery_conn = True
                    break
                else:
                    celery_conn = None
                    raise Exception
            except Exception as e:
                self.stdout.write('Celery unavailable, waiting 1 second {}'.format(str(e)))
                time.sleep(1)
