import pika




def publish():
    connection = pika.BlockingConnection(
    pika.URLParameters('amqps://uebnofyc:hFhiv9SiD_6zOsuhlFfdp_tZGiwC2zcP@shrimp.rmq.cloudamqp.com/uebnofyc'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body='Hellohhhhhhhhhhh World!')
    #print(" [x] Sent 'Hello World!'")
    connection.close()


