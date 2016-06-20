from __future__ import absolute_import

import os

import celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emojinsei.settings')

from django.conf import settings
import socket

#Grab this for later with the local vs web shit

if socket.gethostname().startswith('myhost.local'):
    LIVEHOST = False
else: 
    LIVEHOST = True



 
if LIVEHOST:
	app = celery.Celery('emojinsei',include=['emojinsei.tasks'])

	app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
   
	BROKER_TRANSPORT = 'redis'
else:
    ### LOCAL
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    app = celery.Celery('emojinsei',
             broker='amqp://',
             backend='amqp://',
             include=['emojinsei.tasks'])








# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

#Celery Stuff
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'




# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

if __name__ == '__main__':
    app.start()
