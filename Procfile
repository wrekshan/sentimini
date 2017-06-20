web: gunicorn sentimini.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery -A sentimini worker --beat -c=1
beat: REMAP_SIGTERM=SIGQUIT celery -A sentimini beat -c=1



