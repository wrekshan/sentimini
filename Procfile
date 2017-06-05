web: gunicorn sentimini.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery -A sentimini worker --beat --concurrency=1

