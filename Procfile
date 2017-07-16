web: gunicorn sentimini.wsgi --log-file -
worker1: REMAP_SIGTERM=SIGQUIT celery -A sentimini worker -c=1
worker2: REMAP_SIGTERM=SIGQUIT celery -A sentimini beat -c=1





