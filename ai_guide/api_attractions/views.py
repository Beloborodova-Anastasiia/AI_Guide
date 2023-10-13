import json
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dotenv import load_dotenv

from utilits.open_ai import OpenAiInterract

from api_attractions.consts import MESSAGE, SESTEM_MSG, TEMPERATURE
from attractions.models import Attraction, MisspelledNames
from api_attractions.serializers import AttractionSerializer, QuerySerializer

load_dotenv()

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
            elif attractions_misspeled.exists():
                attraction_misspeled = attractions_misspeled.first()
                attraction = attraction_misspeled.attraction
            else:
                openia_reply = self.get_openia_response(query_name)
                attraction = self.create_attraction_obj(
                    openia_reply, query_name
                )

            reply_serializer = AttractionSerializer(attraction)
            return Response(reply_serializer.data)

        return Response(
            query_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get_openia_response(self, query: str) -> json:
        openai_client = OpenAiInterract(OPENAI_API_KEY)
        message = MESSAGE + f'{query}'
        response = openai_client.get_answer_openai(
            system_msg=SESTEM_MSG,
            user_msg=message,
            temperature=TEMPERATURE
        )
        return json.loads(response)

    def create_attraction_obj(
            self, decode_response: json, query_name: str
    ) -> Attraction:
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
        return attraction
