from django.http import FileResponse
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_guide.settings import MEDIA_ROOT
from api_attractions.serializers import AttractionSerializer, QuerySerializer
from attractions.classes import AttractionInfo
from attractions.models import Attraction, MisspelledNames
from clients.aws_polly_client import AwsPollyClient
from clients.open_ai_client import OpenAiClient

from .const import AUDIO_ERROR_MESSAGE, ERROR_MESSAGE

load_dotenv()

open_ai_client = OpenAiClient()
aws_polly_client = AwsPollyClient()


class AttractionApiView(APIView):

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
                attraction_info = open_ai_client.get_answer(
                    query_name
                )
                if attraction_info:
                    attraction = self.create_attraction_obj(
                        attraction_info, query_name
                    )
                else:
                    return Response(
                        ERROR_MESSAGE, status=status.HTTP_400_BAD_REQUEST
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


class TextToVoiceConverterApiView(APIView):

    def get(self, request, attraction_id):
        attraction = get_object_or_404(Attraction, id=attraction_id)
        try:
            file_name = attraction.object_name
            file = aws_polly_client.get_audio(
                file_name=file_name,
                text=attraction.content
            )
            if file:
                file = open(file, 'rb')
                return FileResponse(file)
            error_file = open(MEDIA_ROOT + '/' + AUDIO_ERROR_MESSAGE, 'rb')
            return FileResponse(error_file)
        except Exception:
            error_file = open(MEDIA_ROOT + '/' + AUDIO_ERROR_MESSAGE, 'rb')
            return FileResponse(error_file)
