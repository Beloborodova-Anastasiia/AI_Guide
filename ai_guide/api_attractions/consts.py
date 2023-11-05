MAX_TOKENS = 3800
MESSAGE = 'Tell me about'
SYSTEM_MSG = """
You are a tour guide. Tell about a touristic attraction in a concise and
simple way, provide factual info. The information should start with the object
geographical position and the approximate time of building.
The story should be minimum 30 words.
Return your answer in the following JSON format without formatting:
'''
{
object_name: "",
location: "",
content: "",
}
'''
"""
TEMPERATURE = 0.6
REGION_NAME = 'eu-west-2'
VOICE_ID = 'Brian'
OUTPUT_FORMAT = 'mp3'
MEDIA_PATH = 'media/audio/'
