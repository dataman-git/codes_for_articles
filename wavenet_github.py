## Text-to-speech Wavenet


import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'YOUR_JSON_FILE.json'

def synthesize_ssml(ssml, 
                    booktitle, 
                    language_code, 
                    voice_name,
                    speaking_rate
                    ):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    Example: <speak>Hello there.</speak>
    """
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate = speaking_rate
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("C:/Users/datas/Downloads/TTS/output/"+booktitle+voice_name+str(speaking_rate)+".mp3", "wb") as out:
        out.write(response.audio_content)
        


# Get the text
import json
folder_path = 'C:/Users/datas/Downloads/TTS/doc/'
booktitle = "Dickens_A_Tale_of_Two_Cities"
filename = folder_path + booktitle + ".txt"
print(filename)
with open(filename, 'r') as f:
    text = f.read()
    f.close()
    print(text)

Emily = synthesize_ssml(text,
    booktitle, 
    language_code = "en-US",
    voice_name = "en-US-Wavenet-E", 
    speaking_rate = 0.8
    )

Frances = synthesize_ssml(text,
    booktitle, 
    language_code = "en-US",
    voice_name = "en-US-Wavenet-F", 
    speaking_rate = 0.8
    )

Adam = synthesize_ssml(text,
    booktitle, 
    language_code = "en-US",
    voice_name = "en-US-Wavenet-A", 
    speaking_rate = 0.8
    )

Jason = synthesize_ssml(text,
    booktitle, 
    language_code = "en-US",
    voice_name = "en-US-Wavenet-J", 
    speaking_rate = 0.8
    )
