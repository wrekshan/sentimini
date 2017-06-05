web: gunicorn sentimini.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery -A sentimini worker --concurrency=1
beat: celery -A sentimini beat --concurrency=1


