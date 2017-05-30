from __future__ import absolute_import

import os

import celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentimini.settings')

from django.conf import settings
import socket

# from sentimini.tasks import schedule_texts, send_texts, check_email_for_new, process_new_mail

#Grab this for later with the local vs web shit

if socket.gethostname().startswith('myhost.local'):
    LIVEHOST = False
else: 
    LIVEHOST = True



 
if LIVEHOST:
	app = celery.Celery('sentimini',include=['sentimini.tasks'])

	app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
   
	BROKER_TRANSPORT = 'redis'

    BROKER_TRANSPORT_OPTIONS = {
        "max_connections": 2,
    }

    # Below is trying to make livehouse like dev
    
else:
    ### LOCAL
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    app = celery.Celery('sentimini',
             broker='amqp://',
             backend='amqp://',
             include=['sentimini.tasks'])


# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=360,
)

#Celery Stuff
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_ALWAYS_EAGER = False

# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

if __name__ == '__main__':
    app.start()

# schedule_texts, send_texts, check_email_for_new, process_new_mail


    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    