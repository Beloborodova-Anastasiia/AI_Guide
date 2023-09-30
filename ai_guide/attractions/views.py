import json
import os

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from get_requests.open_ai import OpenAiInterract

from .consts import SESTEM_MSG
from .models import Attraction
from .serializers import QuirySerializer, AttractionSerializer

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class ApiAnswers(APIView):

    def post(self, request):
        quiry_serializer = QuirySerializer(data=request.data)

        if quiry_serializer.is_valid():
            quiry_name = quiry_serializer.data['quiry']
            attractions = Attraction.objects.filter(
                Q(misataken_names__contains=quiry_name)
                | Q(object_name=quiry_name)
            )

            if attractions.exists():
                attraction = attractions.first()
                print(attraction.object_name)
                

            else:
                openai_client = OpenAiInterract(OPENAI_API_KEY)
                message = f'Tell me about {quiry_name}'
                response = openai_client.get_answer_openai(
                    system_msg=SESTEM_MSG,
                    user_msg=message
                )
                decode_response = json.loads(response)
                attraction = Attraction.objects.create(
                    object_name=decode_response['object_name'],
                    location=decode_response['location'],
                    content=decode_response['content']
                )
                if quiry_name != decode_response['object_name']:
                    attraction.misataken_names.append(quiry_name)
            # print(attraction.object_name)
            # attr = Attraction.objects.all()
            # reply_serializer = AttractionSerializer(attraction)
            # print(reply_serializer.data)
            # data = {
            #     'quiry': message,
            #     'response': response,
            # }
            return Response('data', status=status.HTTP_200_OK)
            # return Response(reply_serializer.data)

        return Response(
            quiry_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
