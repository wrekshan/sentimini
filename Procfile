web: gunicorn sentimini.wsgi --log-file -
beat: REMAP_SIGTERM=SIGQUIT celery -A sentimini --beat --concurrency=1


