web: gunicorn sentimini.wsgi --log-file -
worker: celery -A sentimini worker --beat --concurrency=1

