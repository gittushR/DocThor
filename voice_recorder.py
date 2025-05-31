#Here we record the patient voice and generate the text to be sent to doctor for understanding the issue
import logging
import speech_recognition as sr
from groq import Groq
from pydub import AudioSegment
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

def voice_recorder(file_path,timeout=20,phrase_time_limit=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source,duration=1)
            logging.info("Start speaking now....")

            #Recording the audio
            audio_data = recognizer.listen(source,timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording completed.")

            #Convert the recorded audio to a mp3 file
            wav_data =  audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path,format='mp3',bitrate = '128k')

            logging.info(f"Audio saved to {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error : {e}")

# audio_file_path = 'patient_query.mp3'
# voice_recorder(file_path=audio_file_path)

##Speech to text STT model for transcription
def generate_transcription(audio_file_path):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    audio_file=open(audio_file_path,"rb")
    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        language="en",
    )
    return transcription.text
