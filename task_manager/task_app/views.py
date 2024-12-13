from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .rabbitmq import RabbitMQClient
import json
from django.utils import timezone

# Create your views here.

@api_view(['POST'])
def gateway_message_handler(request):
    try:
        message_type = request.data.get('message_type')
        payload = request.data.get('payload')

        if not message_type or not payload:
            return Response(
                {'error': 'message_type ve payload zorunludur'},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = {
            'message_type': message_type,
            'payload': payload,
            'timestamp': str(timezone.now())
        }

        rabbitmq_client = RabbitMQClient()
        queue_name = f'task_{message_type}_queue' if message_type in ['create', 'update', 'delete'] else 'default_queue'
        rabbitmq_client.publish_message(json.dumps(message), queue_name)

        return Response({'status': 'success', 'message': 'Mesaj kuyruğa gönderildi'})

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class TaskViewSet(viewsets.ModelViewSet):
    """
    Görev API'si için görünüm seti.
    CRUD (Create, Read, Update, Delete) işlemlerini yönetir ve RabbitMQ'ya gönderir.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Görevi veritabanına kaydet
            task = serializer.save()
            
            # RabbitMQ'ya gönderilecek mesajı hazırla
            message = {
                'message_type': 'create',
                'payload': serializer.data,
                'timestamp': str(timezone.now())
            }
            
            # RabbitMQ'ya gönder
            rabbitmq_client = RabbitMQClient()
            rabbitmq_client.publish_message(json.dumps(message), 'task_create_queue')
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Görevi güncelle
            task = serializer.save()
            
            # RabbitMQ'ya gönderilecek mesajı hazırla
            message = {
                'message_type': 'update',
                'payload': serializer.data,
                'timestamp': str(timezone.now())
            }
            
            # RabbitMQ'ya gönder
            rabbitmq_client = RabbitMQClient()
            rabbitmq_client.publish_message(json.dumps(message), 'task_update_queue')
            
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            # RabbitMQ'ya gönderilecek mesajı hazırla
            message = {
                'message_type': 'delete',
                'payload': {'id': kwargs.get('pk')},
                'timestamp': str(timezone.now())
            }
            
            # RabbitMQ'ya gönder
            rabbitmq_client = RabbitMQClient()
            rabbitmq_client.publish_message(json.dumps(message), 'task_delete_queue')
            
            # Görevi sil
            instance.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
