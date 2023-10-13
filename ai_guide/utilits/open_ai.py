# import os
import openai
from dotenv import load_dotenv

load_dotenv()

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class OpenAiInterract:
    MODEL = 'gpt-3.5-turbo'

    def __init__(self, openai_api_key) -> None:
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

    def get_answer_openai(self, system_msg, user_msg, temperature=0.4):
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=temperature,
        )

        return response["choices"][0]['message']['content']
