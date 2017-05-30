web: gunicorn sentimini.wsgi --log-file -
worker: python manage.py celery -A sentimini worker --beat --concurrency=1

