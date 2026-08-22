from django.db import models
from pgvector.django import VectorField

class UIDocumentationChunk(models.Model):
    CATEGORY_CHOICES = [
        ('ui', 'UI Guide'),
        ('api', 'API Docs'),
        ('general', 'General Info'),
    ]

    source_file = models.CharField(max_length=255)  # e.g. "ui_guide.md"
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    embedding = VectorField(dimensions=512) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.category.upper()}] {self.title or 'Chunk'} ({self.source_file})"