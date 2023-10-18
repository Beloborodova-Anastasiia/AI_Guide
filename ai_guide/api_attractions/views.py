import json
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dotenv import load_dotenv

from open_ai_client.open_ai_client import OpenAiClient

from attractions.models import Attraction, MisspelledNames
from api_attractions.serializers import AttractionSerializer, QuerySerializer
from attractions.classes import AttractionInfo

load_dotenv()

openai_client = OpenAiClient()


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
                atrraction_info =  openai_client.get_answer(query_name)
                attraction = self.create_attraction_obj(
                    atrraction_info, query_name
                )

            reply_serializer = AttractionSerializer(attraction)
            return Response(reply_serializer.data)

        return Response(
            query_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def create_attraction_obj(
            self, attraction_info: AttractionInfo, query_name: str
    ) -> Attraction:
        Attraction.objects.get_or_create(
            object_name=attraction_info.object_name,
            location=attraction_info.location,
        )
        attraction = Attraction.objects.get(
            object_name=attraction_info.object_name,
            location=attraction_info.location,
        )
        attraction.content = attraction_info.content
        attraction.save()
        if attraction_info.object_name != query_name:
            MisspelledNames.objects.create(
                misspelled_name=query_name,
                attraction=attraction
            )
        return attraction
