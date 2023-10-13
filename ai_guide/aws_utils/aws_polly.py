import boto3
from contextlib import closing
from dotenv import load_dotenv
import os

# from utils.polly_config import REGION_NAME, VOICE_ID

load_dotenv()
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID'),
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID='AKIAR7A56SB575LZCDVJ'
AWS_SECRET_ACCESS_KEY='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'

class AwsPollyInterract:

    def get_voice(self, region_name: str, voice: str,  text: str, format: str, file: str):
        polly_client = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=region_name).client('polly')

        response = polly_client.synthesize_speech(
            VoiceId=voice,
            OutputFormat=format, 
            Text = text,
        )

        if "AudioStream" in response:
            with closing(response['AudioStream']) as stream:
                output = open(file, 'wb')
                output.write(response['AudioStream'].read())
                output.close()
        
        return file
