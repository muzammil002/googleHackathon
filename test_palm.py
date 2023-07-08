from google.auth import credentials
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from vertexai.preview.language_models import TextGenerationModel

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
import vertexai
import json  # add this line


with open(
    "service_account.json"
) as f:  # replace 'serviceAccount.json' with the path to your file if necessary
    service_account_info = json.load(f)

my_credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)

# Initialize Google AI Platform with project details and credentials
aiplatform.init(
    credentials=my_credentials,
)

with open("service_account.json", encoding="utf-8") as f:
    project_json = json.load(f)
    project_id = project_json["project_id"]


# Initialize Vertex AI with project and location
vertexai.init(project=project_id, location="us-central1")



def handle_chat(temperature: float = .2):
    """
    Endpoint to handle chat.
    Receives a message from the user, processes it, and returns a response from the model.
    """
    model =  TextGenerationModel.from_pretrained("text-bison@001")
    parameters = {
        "temperature": 0.8,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40,
    }
    audio_file='ArianaGrande.m4a'

    # Reads a file as bytes

    response = model.predict(
        '  ,  into text',
        **parameters,
    )
    print(f"Response from Model: {response.text}")
    return {"response": response.text}

if __name__ == "__main__":
    handle_chat()

