from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    
    class Meta:
        fields = ['file_uploaded']
