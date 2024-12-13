import pika
import json
import time

def callback(ch, method, properties, body):
    # Gelen mesajı işle
    message = json.loads(body)
    print(f" [x] Received {message}")
    time.sleep(1)  # İşlem simülasyonu
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consuming():
    # RabbitMQ bağlantı parametreleri
    credentials = pika.PlainCredentials('vicloud01', 'vicloud01')
    parameters = pika.ConnectionParameters(
        host='45.141.151.45',
        port=5672,
        virtual_host='/',
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300
    )
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Queue oluştur
    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Fair dispatch
    channel.basic_qos(prefetch_count=1)
    
    # Callback fonksiyonunu belirle
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    # Mesaj beklemeye başla
    channel.start_consuming()

if __name__ == '__main__':
    try:
        start_consuming()
    except KeyboardInterrupt:
        print('Consumer kapatılıyor...')
    except Exception as e:
        print(f"Hata oluştu: {e}")
