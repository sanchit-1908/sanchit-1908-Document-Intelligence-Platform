
from rest_framework import serializers
from .models import Document
from .models import ChatSession, ChatMessage

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_path']

class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file_type', 'size', 'pages', 'processing_status', 'uploaded_at', 'tags']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'user_message', 'ai_response', 'timestamp']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True, source='chatmessage_set')

    class Meta:
        model = ChatSession
        fields = ['id', 'document', 'created_at', 'messages']