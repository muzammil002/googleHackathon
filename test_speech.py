from google.cloud import speech
import os
import io


def get_transcript(file_name):

    #setting Google credential
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'google_secret.json'
    # create client instance 
    client = speech.SpeechClient()
    transcripts=[]

    #the path of your audio file
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        audio_channel_count=1,
        language_code="en-US",
    )

    # Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})
    # Reads the response
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        transcripts.append("{}".format(result.alternatives[0].transcript))
        
    return transcripts



# if __name__== "__main__":
#     audio='test_audio.wav'
#     get_transcript(audio)