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
    print("NOT LOCAL HOST")
	# app = celery.Celery('sentimini',include=['sentimini.tasks'])
	# app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
 #                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
	# BROKER_TRANSPORT = 'redis'
    
    # CELERY_IMPORTS=("sentimini.tasks")
    # BROKER_URL = os.environ['CLOUDAMQP_URL']
    # BROKER_URL = os.environ['RABBITMQ_BIGWIG_URL']
    CELERY_UTC_ENABLE = True
    BROKER_URL = os.environ['REDIS_URL']
    BROKER_POOL_LIMIT = 1 # Will decrease connection usage
    BROKER_HEARTBEAT = None # We're using TCP keep-alive instead
    BROKER_CONNECTION_TIMEOUT = 30 # May require a long timeout due to Linux DNS timeouts etc
    CELERY_RESULT_BACKEND = None # AMQP is not recommended as result backend as it creates thousands of queues
    CELERY_SEND_EVENTS = False # Will not create celeryev.* queues
    CELERY_EVENT_QUEUE_EXPIRES = 60 # Will delete all celeryev. queues without consumers after 1 minute.
    CELERY_MAX_TASKS_PER_CHILD = 5
    CELERYD_TASK_SOFT_TIME_LIMIT = 60
    
    
    app = celery.Celery('sentimini',
             broker=BROKER_URL,
             # backend='amqp://',
             include=['sentimini.tasks'])

    app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
    # app.conf.broker_transport_options = {'fanout_patterns': True}
    # Below is trying to make livehouse like dev
    
else:
    print("LOCAL HOST")
    # ### LOCAL
    # BROKER_URL = 'amqp://ojkuzlap:AyU-QGhN7CRAmqh-mFmcCyXjrgIvSqZk@orangutan.rmq.cloudamqp.com/ojkuzlap'
    # BROKER_POOL_LIMIT = 1 # Will decrease connection usage
    # BROKER_HEARTBEAT = None # We're using TCP keep-alive instead
    # BROKER_CONNECTION_TIMEOUT = 30 # May require a long timeout due to Linux DNS timeouts etc
    # CELERY_RESULT_BACKEND = None # AMQP is not recommended as result backend as it creates thousands of queues
    # CELERY_SEND_EVENTS = False # Will not create celeryev.* queues
    # CELERY_EVENT_QUEUE_EXPIRES = 60 # Will delete all celeryev. queues without consumers after 1 minute.
    
    # app = celery.Celery('sentimini',
    #          broker='amqp://',
    #          backend='amqp://',
    #          include=['sentimini.tasks'])

    BROKER_URL = 'amqp://guest:guest@localhost:5672//'

    BROKER_POOL_LIMIT = 1 # Will decrease connection usage
    BROKER_HEARTBEAT = None # We're using TCP keep-alive instead
    BROKER_CONNECTION_TIMEOUT = 30 # May require a long timeout due to Linux DNS timeouts etc
    CELERY_RESULT_BACKEND = None # AMQP is not recommended as result backend as it creates thousands of queues
    CELERY_SEND_EVENTS = False # Will not create celeryev.* queues
    CELERY_EVENT_QUEUE_EXPIRES = 60 # Will delete all celeryev. queues without consumers after 1 minute.

    app = celery.Celery('sentimini',
             broker='amqp://',
             backend='amqp://',
             include=['sentimini.tasks'])


# Optional configuration, see the application user guide.
# app.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=360,
#     # CELERYD_MAX_TASKS_PER_CHILD = 100,
#     # CELERY_REDIS_MAX_CONNECTIONS =1,
# )

#Celery Stuff
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
# CELERY_ALWAYS_EAGER = False

# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

if __name__ == '__main__':
    app.start()

# schedule_texts, send_texts, check_email_for_new, process_new_mail


    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    