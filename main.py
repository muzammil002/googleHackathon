from function import process_audio_file
from google.cloud import speech
import os
import io
from google.auth import credentials
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from vertexai.preview.language_models import TextGenerationModel
import vertexai
import json

# Setting Google credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_secret.json'

# Create client instance
client = speech.SpeechClient()

# The path of your audio file
file_name = "test_audio.wav"
output_format = 'mp3'

channels, duration, sample_width, sample_rate, channels_count, output_path = process_audio_file(file_name, output_format)

with io.open(output_path, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_automatic_punctuation=True,
    audio_channel_count=1,
    language_code="en-US",
)

# Sends the request to Google to transcribe the audio
response = client.recognize(request={"config": config, "audio": audio})

# Read the transcript from the response
transcript = ""
for result in response.results:
    transcript += result.alternatives[0].transcript

with open("service_account.json") as f:
    service_account_info = json.load(f)

my_credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Initialize Google AI Platform with project details and credentials
aiplatform.init(credentials=my_credentials)

with open("service_account.json", encoding="utf-8") as f:
    project_json = json.load(f)
    project_id = project_json["project_id"]

# Initialize Vertex AI with project and location
vertexai.init(project=project_id, location="us-central1")

def handle_chat(transcript, temperature=0.2):
    """
    Endpoint to handle chat.
    Receives a message from the user, processes it, and returns a response from the model.
    """
    model = TextGenerationModel.from_pretrained("text-bison@001")
    parameters = {
        "temperature": 0.8,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40,
    }

    # Use the transcript as input for model.predict
    response = model.predict(transcript, **parameters)
    print(f"Response from Model: {response.text}")
    return {"response": response.text}

if __name__ == "__main__":
    handle_chat(transcript)
