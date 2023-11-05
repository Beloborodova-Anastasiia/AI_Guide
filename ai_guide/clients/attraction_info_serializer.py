from rest_framework import serializers


class AttractionInfoSerializer(serializers.Serializer):
    object_name = serializers.CharField(max_length=256)
    location = serializers.CharField(max_length=256)
    content = serializers.CharField(max_length=10000)
