from rest_framework import serializers

from attractions.models import Attraction


class QuerySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    location = serializers.CharField(max_length=256)

    def validate_name(self, obj):
        if len(obj) > 256:
            raise serializers.ValidationError(
                'You name is too long'
            )
        return obj

    def validate_location(self, obj):
        if len(obj) > 256:
            raise serializers.ValidationError(
                'You location is too long'
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
