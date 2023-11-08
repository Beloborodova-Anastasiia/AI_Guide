import json
import os

import openai
from dotenv import load_dotenv

from attractions.classes import AttractionInfo
from clients.attraction_info_serializer import AttractionInfoSerializer
from clients.config import MAX_TOKENS, MESSAGE, MODEL, SYSTEM_MSG, TEMPERATURE

load_dotenv()

OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')


class OpenAiClient:

    def __init__(self) -> None:
        openai.api_key = OPEN_AI_API_KEY

    def get_answer(self, query: str) -> AttractionInfo or None:
        message = MESSAGE + f'{query}'
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
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

            # in the future report to logger 'Open_AI respons is not correct'
            return None
        except Exception:
            return None
        # in the future report to logger
        # 'No answer from Open_AI or answer is not correct'
