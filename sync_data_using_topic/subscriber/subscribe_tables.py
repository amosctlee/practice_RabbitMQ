
import pika
import sys
import logging
from pathlib import Path
import os

TOPICS = os.getenv('SUBSCRIBE_TOPICS')
LOG_DIR = os.getenv('LOG_DIR')
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")

topics = TOPICS.split()
log_dir = Path(LOG_DIR)
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=(log_dir / 'recieved.log').as_posix(),
    level=logging.INFO, 
    format="%(asctime)s %(filename)s %(funcName)s %(lineno)d %(levelname)s: %(message)s", 
    datefmt="%Y%m%d-%H:%M:%S"
    )


logging.info(topics)
logging.info(log_dir)

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = topics
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange=RABBITMQ_EXCHANGE, queue=queue_name, routing_key=binding_key)

logging.info(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    logging.info(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
