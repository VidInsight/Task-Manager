import pika
import json

def check_queues():
    # RabbitMQ bağlantısı
    credentials = pika.PlainCredentials('vicloud02', 'XosW21%f')
    parameters = pika.ConnectionParameters(
        host='45.141.151.45',
        port=5672,
        virtual_host='/',
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Kontrol edilecek kuyruklar
    queues = [
        'request_get_queue',
        'request_post_queue',
        'request_put_queue',
        'request_delete_queue',
        'response_queue'
    ]

    print("\nKuyruk İçerikleri:")
    print("-" * 50)
    
    for queue in queues:
        try:
            # Kuyruk bilgilerini al
            queue_info = channel.queue_declare(queue=queue, passive=True)
            message_count = queue_info.method.message_count
            print(f"\n{queue}: {message_count} mesaj var")

            # Kuyruktan mesajları oku
            while True:
                method_frame, header_frame, body = channel.basic_get(queue=queue)
                if not method_frame:
                    break
                    
                print("\nMesaj:")
                try:
                    message = json.loads(body)
                    print(json.dumps(message, indent=2, ensure_ascii=False))
                except:
                    print(body)
                    
                # Mesajı kuyruktan sil
                channel.basic_ack(method_frame.delivery_tag)
                
        except Exception as e:
            print(f"{queue}: Hata - {str(e)}")

    connection.close()

if __name__ == "__main__":
    print("RabbitMQ kuyrukları kontrol ediliyor...")
    check_queues()
