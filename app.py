##
# 
##

from flask import Flask, jsonify, render_template, request
import os
import pika
import sys
from slugify import slugify

# Flask setup and config
app = Flask(__name__)

# Heroku creates this environment variable that points at
# the amqp:// URI. I grab it from the environment and throw
# in as a config variable in flask. If it doesn't exist,
# let's bail out, since we need this in order to pipe things.
app.config['RABBITMQ_BIGWIG_TX_URL'] = \
    os.environ.get('RABBITMQ_BIGWIG_TX_URL', None)

if app.config['RABBITMQ_BIGWIG_TX_URL'] is None:
    print('Set RABBITMQ_BIGWIG_TX_URL!')
    sys.exit(1)

# This sends a message to a RMQ queue; if everything goes well,
# send a status message. Otherwise, let's be crazy and return
# False
def pipe_message(message, queue):
    if message is None or message == '':
        return False

    if queue is None or queue == '':
        queue = 'default'

    queue = slugify(queue)
    
    try:
        connection = pika.BlockingConnection(
            pika.URLParameters(app.config['RABBITMQ_BIGWIG_TX_URL'])
        )
        channel = connection.channel()

        queue_name = 'queue_%s' % queue
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message,
                              properties=pika.BasicProperties(
                                delivery_mode = 2,
                              ))

        connection.close()

        return 'submitted to queue %s' % queue
    except Exception as e:
        print(e)
        return False


@app.route('/pipe', methods=['POST'])
@app.route('/pipe/<queue>', methods=['POST'])
def pipe(queue='default'):
    json = request.get_json()
    content = json.get('content')

    response = pipe_message(content, queue)

    if response is not False:
        return jsonify({
            'status': 'ok',
            'message': response
        })
    else:
        return jsonify({
            'status': 'error'
        })


@app.route('/', methods=['GET', 'POST'])
def home():
    errors = []
    notifications = []

    if request.method == 'POST':
        message = request.form.get('content')
        name = request.form.get('name')

        response = pipe_message(message, name)
        
        if response is not False:
            notifications.append(response)
        else:
            errors.append('an error occured')
            return render_template('hello.html', errors=errors)

    return render_template('hello.html', notifications=notifications)


@app.route('/slides')
def slides():
    return app.send_static_file('slides.html')
