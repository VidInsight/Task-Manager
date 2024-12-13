import pika
import json
from django.utils import timezone

class RabbitMQClient:
    """
    RabbitMQ ile iletişim kurmak için kullanılan istemci sınıfı.
    Bu sınıf, mesaj kuyruğu işlemlerini yönetir.
    """
    def __init__(self):
        """
        İstemci başlatıldığında çalışan yapıcı metod.
        """
        self.connection = None
        self.channel = None
        self.queues = {
            'request_get_queue': {'durable': True},
            'request_post_queue': {'durable': True},
            'request_put_queue': {'durable': True},
            'request_delete_queue': {'durable': True},
            'request_patch_queue': {'durable': True},
            'response_queue': {'durable': True},
            'default_queue': {'durable': True}
        }
        self.connect()

    def connect(self):
        """
        RabbitMQ sunucusuna bağlantı kurar.
        """
        try:
            credentials = pika.PlainCredentials('vicloud02', 'XosW21%f')
            parameters = pika.ConnectionParameters(
                host='45.141.151.45',
                port=5672,
                virtual_host='/',
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Tüm kuyrukları oluştur
            for queue_name, options in self.queues.items():
                self.channel.queue_declare(queue=queue_name, **options)
                
        except Exception as e:
            print(f"RabbitMQ bağlantı hatası: {str(e)}")
            raise

    def publish_message(self, message, queue_name='default_queue'):
   
        try:
        
            if not isinstance(message, (str, bytes)):
                message = json.dumps(message)

            # Kuyruk yoksa oluştur
            if queue_name not in self.queues:
                self.channel.queue_declare(queue=queue_name, durable=True)
                self.queues[queue_name] = {'durable': True}

            # Mesajı gönder
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # mesajı kalıcı hale getirir
                    timestamp=int(timezone.now().timestamp()),
                    content_type='application/json'
                )
            )
            print(f"Mesaj {queue_name} kuyruğuna gönderildi: {message}")
            return True
        except Exception as e:
            print(f"Mesaj gönderme hatası: {str(e)}")
            if not self.connection or self.connection.is_closed:
                self.connect()  # Bağlantı kopmuşsa yeniden bağlan
            return False

    def close(self):
        """
        RabbitMQ bağlantısını güvenli bir şekilde kapatır.
        """
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def __del__(self):
        self.close()
