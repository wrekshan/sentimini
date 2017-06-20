web: gunicorn sentimini.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery -A sentimini worker -c=1
beat: REMAP_SIGTERM=SIGQUIT celery -A sentimini -B -c=1




