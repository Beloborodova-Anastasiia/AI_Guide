import boto3
from contextlib import closing
from dotenv import load_dotenv
import os

# from utils.polly_config import REGION_NAME, VOICE_ID
from ai_guide.settings import MEDIA_ROOT

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


class AwsPollyInterract:

    def get_voice(
            self,
            region_name: str,
            voice: str,
            text: str,
            format: str,
            file: str
    ):

        polly_client = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=region_name).client('polly')

        response = polly_client.synthesize_speech(
            VoiceId=voice,
            OutputFormat=format,
            Text=text,
        )
        if "AudioStream" in response:
            with closing(response['AudioStream']) as stream:
                output = open(MEDIA_ROOT + '/' + file, 'wb')
                output.write(stream.read())
                output.close()

        return output.name
