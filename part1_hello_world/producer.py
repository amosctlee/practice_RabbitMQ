import pika

# https://pika.readthedocs.io/en/stable/modules/parameters.html#pika.connection.ConnectionParameters

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')


channel.basic_publish(exchange='',  # default exchange identified by an empty string
                      routing_key='hello',  # queue name
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")


connection.close()