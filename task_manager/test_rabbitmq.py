import pika
import json

def send_message_to_queue(message):
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

    # Mesajı JSON formatına çevir
    message_body = json.dumps(message)

    # Mesajı gönder
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message_body,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Mesajı kalıcı hale getirir
        )
    )

    print(f" [x] Sent {message}")
    connection.close()

# Test mesajı
test_message = {
    "task_type": "create_task",
    "title": "Test Task",
    "description": "This is a test task",
    "priority": "high",
    "due_date": "2024-12-14"
}

if __name__ == "__main__":
    try:
        send_message_to_queue(test_message)
        print("Mesaj başarıyla gönderildi!")
    except Exception as e:
        print(f"Hata oluştu: {e}")
