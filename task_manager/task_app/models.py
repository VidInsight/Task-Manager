from django.db import models
class Task(models.Model):
    """
    Görev bilgilerini tutan model sınıfı.
    Her bir görev için başlık, açıklama, durum ve zaman bilgilerini saklar.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),      # Beklemede
        ('processing', 'Processing'), # İşleniyor
        ('completed', 'Completed'),   # Tamamlandı
        ('failed', 'Failed'),        # Başarısız
    ]

    # Görev başlığı (zorunlu alan)
    title = models.CharField(max_length=200)
    
    # Görev açıklaması (isteğe bağlı alan)
    description = models.TextField()
    
    # Görevin mevcut durumu (varsayılan: beklemede)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Oluşturulma zamanı (otomatik eklenir)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Son güncelleme zamanı (her değişiklikte otomatik güncellenir)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Model örneğinin string gösterimi
        Returns:
            str: "Görev Başlığı - Durum" formatında
        """
        return f"{self.title} - {self.status}"
