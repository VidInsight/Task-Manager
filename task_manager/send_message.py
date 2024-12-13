import pika
import json

# Bağlantı parametreleri
credentials = pika.PlainCredentials('vicloud01', 'vicloud01')
parameters = pika.ConnectionParameters(
    host='45.141.151.45',
    port=5672,
    virtual_host='/',
    credentials=credentials,
    heartbeat=600,
    blocked_connection_timeout=300
)

try:
    # Bağlantı oluştur
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Test mesajı
    message = {
        "task_type": "create",
        "data": {
            "title": "Test Task",
            "description": "Test Description"
        }
    }

    # Mesajı gönder
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type='application/json'
        )
    )

    print("Mesaj başarıyla gönderildi!")
    connection.close()

except Exception as e:
    print(f"Hata oluştu: {str(e)}")
