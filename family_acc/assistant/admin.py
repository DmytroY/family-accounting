from django.contrib import admin

from .models import UIDocumentationChunk

@admin.register(UIDocumentationChunk)
class UIDocumentationChunkAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'source_file', 'title', 'created_at')
    list_filter = ('category', 'source_file')
    search_fields = ('content', 'title')
