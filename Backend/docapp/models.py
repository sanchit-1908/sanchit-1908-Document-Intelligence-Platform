
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=50)  # e.g., pdf, docx, txt, md
    size = models.IntegerField()  # in bytes
    pages = models.IntegerField()
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list)  # searchable tags
    processing_status = models.CharField(max_length=50, default='pending')  # pending, processed, failed
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    chunk_index = models.IntegerField()
    text = models.TextField()
    page_number = models.IntegerField()
    start_char = models.IntegerField(null=True, blank=True)
    end_char = models.IntegerField(null=True, blank=True)
    chunk_type = models.CharField(max_length=50, default='semantic')  # semantic, window, paragraph, etc.
    embedding_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"


class ChatSession(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} for {self.document.title}"


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    source_chunks = models.JSONField(default=list)  # list of chunk indices or IDs used for answer

    def __str__(self):
        return f"Q: {self.user_message[:30]}... | A: {self.ai_response[:30]}..."
