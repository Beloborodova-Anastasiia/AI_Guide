# from typing import Dict, List
# import json

# from pip._vendor import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()
# openai.organization = 'AI-Guide'

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.Model.list()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ENDPOINT = 'https://api.openai.com/v1/chat/completions'

# HEADERS = {
#     "Content-Type: application/json",
#     "Authorization: Bearer {OPENAI_API_KEY}"
# }

# PARAMS = {
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "user", "content": "Say this is a test!"}],
#     "temperature": 0.4
# }


def get_answer_openai(system_msg, user_msg, model='gpt-3.5-turbo'):
    response = openai.ChatCompletion.create(
        model=model,
        # prompt=prompt,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        # max_tokens=100,
        # n=1,
        # stop=None,
        temperature=0.4,
    )

    # message = response.choices[0].text.strip()
    return response


items = get_answer_openai(
    'Write friendly way',
    'Write "Hello world" in Russian and Franch')
print(items)
