web: gunicorn sentimini.wsgi --log-file -
worker: celery -A sentimini worker -B --concurrency=1

