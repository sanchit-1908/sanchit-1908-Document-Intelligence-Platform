from django.shortcuts import render

# Create your views here.
import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from .models import Document
from .serializers import DocumentUploadSerializer

import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from .models import Document
from .serializers import DocumentUploadSerializer
from docapp.processing import process_document  # ✅ Import the engine

# from rest_framework.parsers import MultiPartParser, FormParser

class DocumentUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['file_path']
            title = request.data.get('title', file.name)
            description = request.data.get('description', '')

            tags_raw = request.data.get('tags', '[]')
            try:
                tags = json.loads(tags_raw) if isinstance(tags_raw, str) else tags_raw
            except json.JSONDecodeError:
                tags = []

            file_type = os.path.splitext(file.name)[1].lower().replace('.', '')
            size = file.size

            # Step 1: Page count extraction (before saving to satisfy NOT NULL constraint)
            pages = 1
            try:
                if file_type == 'pdf':
                    reader = PdfReader(file)
                    pages = len(reader.pages)
                elif file_type == 'docx':
                    doc = DocxDocument(file)
                    pages = len(doc.paragraphs)
                elif file_type in ['txt', 'doc']:
                    pages = 1
            except Exception:
                pages = 1

            # Step 2: Save file & DB entry
            temp_doc = serializer.save(
                title=title,
                file_path=file,
                file_type=file_type,
                size=size,
                pages=pages,
                description=description,
                tags=tags,
                processing_status='uploaded'
            )

            # Step 3: Run the processing engine
            try:
                process_document(temp_doc)
                temp_doc.processing_status = 'processed'
            except Exception as e:
                print("Processing error:", e)
                temp_doc.processing_status = 'failed'

            temp_doc.save()

            return Response(DocumentUploadSerializer(temp_doc).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# docapp/views.py

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Document
from .serializers import DocumentListSerializer

class DocumentListView(generics.ListAPIView):
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentListSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['file_type', 'processing_status']  # filter by type or status
    search_fields = ['title', 'description', 'tags']        # search by text fields


from rest_framework import generics
from .models import Document
from .serializers import DocumentListSerializer

class DocumentDetailView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentListSerializer
    lookup_field = 'id'


# docapp/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from .models import Document

class DocumentDeleteView(generics.DestroyAPIView):
    queryset = Document.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        document = self.get_object()
        file_path = document.file_path.path  # get absolute file path

        # Delete the DB record
        self.perform_destroy(document)

        # Optional: Delete the physical file
        if os.path.exists(file_path):
            os.remove(file_path)

        return Response({"message": "Document deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document, ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from .processing.rag import answer_query  # Import your RAG engine
import traceback
from openai import OpenAI

from openai._exceptions import OpenAIError, RateLimitError




class ChatView(APIView):
    def post(self, request, document_id, *args, **kwargs):
        print(f"Received POST to ChatView with document_id: {document_id}")
        
        try:
            document = Document.objects.get(id=document_id)
            session, _ = ChatSession.objects.get_or_create(document=document)
            
            if not (user_message := request.data.get('message')):
                return Response({"detail": "Message content is required."}, status=400)

            try:
                ai_response = answer_query(user_message)
                print(f"Successful AI response for document {document_id}")
                
                chat_message = ChatMessage.objects.create(
                    session=session,
                    user_message=user_message,
                    ai_response=ai_response
                )
                return Response(ChatMessageSerializer(chat_message).data, status=201)
                
            except RateLimitError:
                return Response({
                    "detail": "API quota exceeded. Please try again later or check your OpenAI account.",
                    "solution": "1. Check usage at platform.openai.com/usage\n2. Upgrade your plan if needed"
                }, status=429)
                
            except Exception as e:
                print(f"Error processing query: {str(e)}")
                return Response({
                    "detail": "Failed to generate response",
                    "error": str(e)
                }, status=500)

        except Document.DoesNotExist:
            return Response({"detail": "Document not found."}, status=404)
        


# views.py
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView

class DocumentContentView(APIView):
    def get(self, request, document_id):
        document = Document.objects.get(id=document_id)
        
        if document.file_type == 'pdf':
            return FileResponse(open(document.file_path.path, 'rb'), content_type='application/pdf')
        
        # For text-based files
        try:
            with open(document.file_path.path, 'r') as f:
                content = f.read()
            return JsonResponse({'content': content})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)