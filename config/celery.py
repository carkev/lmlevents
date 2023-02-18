import os
import kombu
from celery import Celery, bootsteps

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config', broker="amqp://admin:admin@broker//")
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# setting publisher
with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='exchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()
    queue = kombu.Queue(
        name='queue',
        exchange=exchange,
        routing_key='mykey',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()

# setting consumer class
class MyConsumerStep(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[queue],
                               callbacks=[self.handle_message],
                               accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        message.ack()

# Register the custom consumer
app.steps['consumer'].add(MyConsumerStep)
