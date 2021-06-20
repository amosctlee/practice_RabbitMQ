import time
import pika
import sys, os

# https://pika.readthedocs.io/en/stable/modules/parameters.html#pika.connection.ConnectionParameters

def main():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    # channel.queue_declare(queue='hello')

    # 實驗三
    channel.queue_declare(queue='task_queue', durable=True)


    # Whenever we receive a message, this callback function is called by the Pika library
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")

        # 實驗二 要加上
        ch.basic_ack(delivery_tag = method.delivery_tag)

    # channel.basic_consume(queue='hello', 
    #                     # auto_ack=True,  # 實驗二要註解
    #                     on_message_callback=callback)

    # 實驗四
    channel.basic_qos(prefetch_count=1)
    # 實驗三
    channel.basic_consume(queue='task_queue', 
                        # auto_ack=True,  # 實驗二要註解
                        on_message_callback=callback)


    # And finally, we enter a never-ending loop that waits for data 
    # and runs callbacks whenever necessary, and catch KeyboardInterrupt 
    # during program shutdown.
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)