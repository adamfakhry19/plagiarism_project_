from rest_framework import serializers

class PlagiarismResultSerializer(serializers.Serializer):
    file1 = serializers.CharField(max_length=255)
    file2 = serializers.CharField(max_length=255)
    score = serializers.FloatField()
