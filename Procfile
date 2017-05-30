web: gunicorn sentimini.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery senitmini worker --loglevel=info --concurrency=1
celery_beat: celery sentimini beat --loglevel=info --concurrency=1

