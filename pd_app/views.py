# from django.shortcuts import render, redirect  # Remove this if not used elsewhere
import os
from collections import defaultdict
from pd_app.pd_model import predict_plagiarism
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import PlagiarismResultSerializer

def handle_uploaded_file(f):
    file_path = os.path.join('media', f.name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        for file in files:
            handle_uploaded_file(file)

        uploaded_files = [os.path.join('media', f) for f in os.listdir('media') if os.path.isfile(os.path.join('media', f))]
        uploaded_files.sort()

        if len(uploaded_files) < 2:
            return Response({'error': 'Please upload at least two files.'}, status=status.HTTP_400_BAD_REQUEST)

        pairwise_scores = []

        for i in range(len(uploaded_files)):
            for j in range(i + 1, len(uploaded_files)):
                file1 = uploaded_files[i]
                file2 = uploaded_files[j]
                score = predict_plagiarism(file1, file2)
                pairwise_scores.append({
                    'file1': os.path.basename(file1),
                    'file2': os.path.basename(file2),
                    'score': score
                })

        serializer = PlagiarismResultSerializer(pairwise_scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
