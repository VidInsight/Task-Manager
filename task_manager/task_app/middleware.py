import json
from django.utils import timezone
from .rabbitmq import RabbitMQClient

class RequestQueueMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rabbitmq_client = RabbitMQClient()

    def __call__(self, request):
        # İstek bilgilerini hazırla
        request_data = {
            'method': request.method,
            'path': request.path,
            'query_params': dict(request.GET),
            'body': self._get_request_body(request),
            'headers': dict(request.headers),
            'timestamp': str(timezone.now())
        }

        # RabbitMQ'ya gönder
        try:
            queue_name = f'request_{request.method.lower()}_queue'
            self.rabbitmq_client.publish_message(
                message=request_data,
                queue_name=queue_name
            )
        except Exception as e:
            print(f"RabbitMQ'ya gönderme hatası: {str(e)}")

        # Normal request-response döngüsüne devam et
        response = self.get_response(request)

        # Yanıt bilgilerini hazırla ve gönder
        response_data = {
            'status_code': response.status_code,
            'content': self._get_response_content(response),
            'headers': dict(response.headers),
            'timestamp': str(timezone.now())
        }

        try:
            self.rabbitmq_client.publish_message(
                message=response_data,
                queue_name='response_queue'
            )
        except Exception as e:
            print(f"RabbitMQ'ya yanıt gönderme hatası: {str(e)}")

        return response

    def _get_request_body(self, request):
        """İstek gövdesini almak için yardımcı metod"""
        try:
            if request.body:
                return json.loads(request.body)
        except:
            pass
        return {}

    def _get_response_content(self, response):
        """Yanıt içeriğini almak için yardımcı metod"""
        try:
            return response.content.decode('utf-8')
        except:
            return str(response.content)
