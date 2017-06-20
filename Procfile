web: gunicorn sentimini.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery -A sentimini worker -B -c=1
beat: celery -A sentimini beat -c=1


