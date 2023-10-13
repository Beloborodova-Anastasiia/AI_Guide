from dotenv import load_dotenv
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
            self.get_awas_polly_response(attraction)
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
