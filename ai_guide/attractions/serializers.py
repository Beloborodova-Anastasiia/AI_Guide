from rest_framework import serializers

from .models import Attraction


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=256)


class AttractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attraction
        fields = (
            'id',
            'object_name',
            'location',
            'content',
        )
