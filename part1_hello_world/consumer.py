import pika
import sys, os

# https://pika.readthedocs.io/en/stable/modules/parameters.html#pika.connection.ConnectionParameters

def main():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hello')


    # Whenever we receive a message, this callback function is called by the Pika library
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello',
                        auto_ack=True,
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