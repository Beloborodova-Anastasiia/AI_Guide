from dotenv import load_dotenv
import json
import os

from django.core.files import File
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_attractions.serializers import AttractionSerializer, QuerySerializer
from attractions.classes import AttractionInfo
from attractions.models import Attraction, MisspelledNames
from open_ai_client.open_ai_client import OpenAiClient

load_dotenv()

open_ai_client = OpenAiClient()


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
                atrraction_info = open_ai_client.get_answer(query_name)
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
        # self.get_awas_polly_response(attraction)
        if attraction_info.object_name != query_name:
            MisspelledNames.objects.create(
                misspelled_name=query_name,
                attraction=attraction
            )
        return attraction

    def add_aws_polly_response_to_attraction(self, attraction):
        polly = AwsPollyInterract()
        file_name = attraction.object_name
        returned_file = polly.get_voice(
            voice=VOICE_ID,
            format=OUTPUT_FORMAT,
            region_name=REGION_NAME,
            file=f'{file_name}.{OUTPUT_FORMAT}',
            text=attraction.content
        )
    
        with open(returned_file, 'rb') as file:
            file_for_model = File(file)
            attraction.audio = file_for_model
            attraction.save()
            file.close()
            os.remove(returned_file)


class GetAudio(APIView):

    def get(self, request, id):
        attraction = get_object_or_404(Attraction, id=id)
        return FileResponse(attraction.audio.open())


        


