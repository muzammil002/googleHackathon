from google.auth import credentials
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
from vertexai.preview.language_models import TextGenerationModel
import vertexai
import json  # add this line
from test_speech import get_transcript

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



def handle_chat(temperature: float = .6):
    """
    Endpoint to handle chat.
    Receives a message from the user, processes it, and returns a response from the model.
    """
    model =  TextGenerationModel.from_pretrained("text-bison@001")
    parameters = {
        "temperature": 0.4,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40,
    }

    # Reads a file as bytes
    transcript= get_transcript('test_audio.wav')
    transcript_text = " ".join(transcript)
    if transcript is not None:  
        print(transcript_text)
        response = model.predict(
            f"whats going on  in the context. :\n\n{transcript_text}",
            **parameters,
        )
    print(f"Response from Model: {response.text}")
    return {"response": response.text}


if __name__ == "__main__":
    handle_chat()

