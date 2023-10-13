import json
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dotenv import load_dotenv

from open_ai_utils.open_ai import OpenAiInterract
from aws_utils.aws_polly import AwsPollyInterract

from api_attractions.consts import (MESSAGE, SESTEM_MSG, TEMPERATURE, OUTPUT_FORMAT, VOICE_ID,
                                    REGION_NAME, MEDIA_PATH)
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
            self.get_awas_polly_response(attraction)
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
        # self.get_awas_polly_response(attraction)
        if decode_response['object_name'] != query_name:
            MisspelledNames.objects.create(
                misspelled_name=query_name,
                attraction=attraction
            )
        return attraction

    def get_awas_polly_response(self, attraction):
        print('!!!!!!')
        polly = AwsPollyInterract()
        file = polly.get_voice(
            voice=VOICE_ID,
            format=OUTPUT_FORMAT,
            region_name=REGION_NAME,
            file=MEDIA_PATH + f'{attraction.object_name}.{OUTPUT_FORMAT}',
            text=attraction.content
        )
        print(file, '!!!!!!!!!')
        # attraction.audio = file
        # attraction.save()
        # with open(file, 'rb') as fi:
        #     self.my_file = File(fi, name=os.path.basename(fi.name))
        #     self.save()
