import os
from contextlib import closing

import boto3
from dotenv import load_dotenv

from ai_guide.settings import MEDIA_ROOT

from .config import OUTPUT_FORMAT, REGION_NAME, VOICE_ID

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


class AwsPollyClient:

    def get_audio(self, text: str, file_name: str):
        try:
            polly_client = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=REGION_NAME).client('polly')

            response = polly_client.synthesize_speech(
                VoiceId=VOICE_ID,
                OutputFormat=OUTPUT_FORMAT,
                Text=text,
            )
            if 'AudioStream' in response:
                with closing(response['AudioStream']) as stream:
                    output = open(
                        MEDIA_ROOT + '/' + f'{file_name}.{OUTPUT_FORMAT}', 'wb'
                    )
                    output.write(stream.read())
                    output.close()
                return output.name
            else:
                raise Exception('No AudioStream in response')
        except Exception:
            raise Exception(
                'No answer from AWS_Polly or answer is not correct'
            )
