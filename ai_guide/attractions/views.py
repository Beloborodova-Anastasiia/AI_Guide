import json
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from get_requests.open_ai import OpenAiInterract

from .consts import SESTEM_MSG
from .models import Attraction, MisspelledNames
from .serializers import AttractionSerializer, QuerySerializer

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class ApiAnswers(APIView):

    def post(self, request):
        query_serializer = QuerySerializer(data=request.data)

        if query_serializer.is_valid():
            query_name = query_serializer.data['query']
            attractions = Attraction.objects.filter(
                object_name=query_name
            )
            attractions_misspeled = MisspelledNames.objects.filter(
                misspelled_name=query_name
            )
            if attractions.exists():
                attraction = attractions.first()
                # print('From Attractions', attraction)
            elif attractions_misspeled.exists():
                attraction_misspeled = attractions_misspeled.first()
                attraction = attraction_misspeled.attraction
                # print('From MisspelledNames', attraction)
            else:
                openai_client = OpenAiInterract(OPENAI_API_KEY)
                message = f'Tell me about {query_name}'
                response = openai_client.get_answer_openai(
                    system_msg=SESTEM_MSG,
                    user_msg=message
                )
                decode_response = json.loads(response)
                Attraction.objects.get_or_create(
                    object_name=decode_response['object_name'],
                    location=decode_response['location'],
                )
                attraction = Attraction.objects.get(
                    object_name=decode_response['object_name'],
                    location=decode_response['location'],
                )
                attraction.content = decode_response['content']
                attraction.save()
                if decode_response['object_name'] != query_name:
                    MisspelledNames.objects.create(
                        misspelled_name=query_name,
                        attraction=attraction
                    )
                # print('From open_AI', attraction)
            reply_serializer = AttractionSerializer(attraction)
            return Response(reply_serializer.data)

        return Response(
            query_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
