from rest_framework import serializers

from attractions.models import Attraction


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=256)

    def validate_query(self, obj):
        if len(obj) > 256:
            raise serializers.ValidationError(
                'You query is too long'
            )
        return obj


class AttractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attraction
        fields = (
            'id',
            'object_name',
            'location',
            'content',
        )
