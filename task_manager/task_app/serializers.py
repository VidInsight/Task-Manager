from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Task modeli için serileştirici sınıf.
    API isteklerinde gelen JSON verisini Task modeline,
    Task modelini de JSON verisine dönüştürür.
    
    Alanlar:
    - id: Görevin benzersiz kimliği (otomatik)
    - title: Görev başlığı
    - description: Görev açıklaması
    - status: Görevin durumu
    - created_at: Oluşturulma zamanı (salt okunur)
    - updated_at: Güncellenme zamanı (salt okunur)
    """
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']  # Bu alanlar sadece okunabilir
