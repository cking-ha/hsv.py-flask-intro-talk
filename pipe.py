#!/usr/bin/env python
import pika
import signal
from sys import argv, exit

# signal handler code
def handler(signal, frame):
    exit()

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

# callback to give to the consume function
def get_messages(ch, method, properties, body):
    print(body.decode("UTF-8"))

# basic argument handler
if len(argv) < 2 or len(argv) > 3:
    print("Usage: {} AMQP_URI [QUEUE_NAME]".format(argv[0]))
    exit(1)

amqp_uri = argv[1]
queue = argv[2] if 2 < len(argv) else 'default'
queue = 'queue_%s' % queue

# try to set up and use the connection
try:
    parameters = pika.URLParameters(amqp_uri)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    channel.basic_consume(get_messages, queue=queue, no_ack=True)
    channel.start_consuming()
except Exception as e:
    print(e)
