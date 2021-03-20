import os
import pika
import sys


def send():
    connection = pika.BlockingConnection(
        pika.URLParameters('amqps://fkeozvxu:XUux19JAykFYZR7D2WmNuURddzKZwIag@hawk.rmq.cloudamqp.com/fkeozvxu'))
    channel = connection.channel()

    channel.queue_declare(queue='kashapov')

    # message = ' '.join(sys.argv[1:]) or "shakhov\n"
    # channel.basic_publish(
    #     exchange='',
    #     routing_key='kashapov',
    #     body=message,
    #     )
    # print(" [x] Sent %r" % message)

    channel.basic_publish(exchange='', routing_key='kashapov', body='shakhov\n')
    print(" [x] Sent 'Yury'")
    connection.close()


def recieve():
    connection = pika.BlockingConnection(pika.URLParameters('amqps://fkeozvxu:XUux19JAykFYZR7D2WmNuURddzKZwIag@hawk.rmq.cloudamqp.com/fkeozvxu'))
    channel = connection.channel()

    channel.queue_declare(queue='shakhov')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='shakhov', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        if recieve():
            send()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
