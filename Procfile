web: gunicorn sentimini.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUI celery -A sentimini worker -B --concurrency=1

