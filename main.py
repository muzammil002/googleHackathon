from function import process_audio_file, get_transcript
from vertexai.preview.language_models import TextGenerationModel
import vertexai
import json
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform

def handle_chat(temperature=0.2):
    """
    Endpoint to handle chat.
    Receives a message from the user, processes it, and returns a response from the model.
    """
    # The path of your audio file
    file_name = "test_audio.wav"
    output_format = 'wav'

    channels, duration, sample_width, sample_rate, channels_count, output_path = process_audio_file(file_name, output_format)

    # Extract the transcript using the get_transcript function
    print(output_path)
    transcript = get_transcript(output_path)
    transcript_text = " ".join(transcript)
    print(transcript)

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

    model = TextGenerationModel.from_pretrained("text-bison@001")
    parameters = {
        "temperature": 0.8,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40,
    }

    
    if transcript is not None:
        print(transcript_text)
        response = model.predict(
            f"what's going on in the context:\n\n{transcript_text}",
            **parameters,
        )
        print(f"Response from Model: {response.text}")
        return {"response": response.text}
    else:
        return {"response": "No transcript found."}

if __name__ == "__main__":
    handle_chat()
