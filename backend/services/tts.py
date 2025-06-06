from gtts import gTTS
import os
from io import BytesIO

def text_to_speech(text,output_path):
    tts = gTTS(text)
    tts.save(output_path)

#using BytesIO so that I can use this in the db.py gridfs store
def text_to_speech_bytes(text: str) -> bytes:
    tts = gTTS(text)
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer.read()

#testing
if __name__ == "__main__":

    text_to_speech("through the columns of the esteemed newspaper I would like to draw the attention of the government to the plight of the people of the country","test.mp3")
