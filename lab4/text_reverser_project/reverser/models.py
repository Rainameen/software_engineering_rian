from django.db import models
from django.utils import timezone

class TextEntry(models.Model):
    original_text = models.TextField(verbose_name="النص الأصلي")
    reversed_text = models.TextField(verbose_name="النص المعكوس")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "إدخال نص"
        verbose_name_plural = "إدخالات النصوص"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.original_text[:50]}..." if len(self.original_text) > 50 else self.original_text
    
    def save(self, *args, **kwargs):
        # عكس النص تلقائياً عند الحفظ
        self.reversed_text = self.original_text[::-1]
        super().save(*args, **kwargs)
