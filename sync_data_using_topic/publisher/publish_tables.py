import pika
import sys
import os 

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")


credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='topic')

while True:
    from_input = input("plz input topic and messages: ")
    from_input = from_input.split()

    routing_key = from_input[0] if len(from_input) > 1 else 'anonymous.info'
    message = ' '.join(from_input[1:]) or 'Hello World!'
    channel.basic_publish(
        exchange=RABBITMQ_EXCHANGE, routing_key=routing_key, body=message)

    print(" [x] Sent %r:%r" % (routing_key, message))

connection.close()