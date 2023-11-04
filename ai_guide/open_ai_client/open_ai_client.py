import json
import os

import openai
from dotenv import load_dotenv
from rest_framework import serializers

from api_attractions.consts import MAX_TOKENS, MESSAGE, SYSTEM_MSG, TEMPERATURE
from attractions.classes import AttractionInfo
from open_ai_client.serizalizers import AttractionInfoSerializer

load_dotenv()

OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')


class OpenAiClient:
    MODEL = 'gpt-3.5-turbo'

    def __init__(self) -> None:
        openai.api_key = OPEN_AI_API_KEY

    def get_answer(self, query: str) -> AttractionInfo:
        message = MESSAGE + f'{query}'
        try:
            response = openai.ChatCompletion.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_MSG},
                    {"role": "user", "content": message}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            serializer = AttractionInfoSerializer(
                data=json.loads(response["choices"][0]['message']['content'])
            )
            if serializer.is_valid():
                attraction_info = AttractionInfo(
                    object_name=serializer.data['object_name'],
                    location=serializer.data['location'],
                    content=serializer.data['content']
                )
                return attraction_info

            raise serializers.ValidationError(
                'Open_AI respons is not correct'
            )
        except Exception:
            raise Exception('No answer from Open_AI or answer is not correct')
