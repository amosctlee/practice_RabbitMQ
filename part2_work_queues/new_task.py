import pika
import sys

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

# channel.queue_declare(queue='hello')

# 實驗三
channel.queue_declare(queue='task_queue', durable=True)


message = ' '.join(sys.argv[1:]) or "Hello World!"
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body=message)


# 實驗三
channel.basic_publish(exchange='',
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

print(" [x] Sent %r" % message)

connection.close()