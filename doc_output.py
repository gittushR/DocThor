#This file will convert the doctor analysis into doctors voice to be played after analysisGe
#text to speech translate
from gtts import gTTS
import subprocess
from pydub import AudioSegment

def text_to_speech(text,output_filepath):
    audio_obj = gTTS(
        text=text,
        lang="en",
        slow=False,
        tld="co.in"
    )
    audio_obj.save(output_filepath)
    sound = AudioSegment.from_mp3(output_filepath)
    sound.export("final.wav",format='wav')
    print(output_filepath)
    try:
        subprocess.run(['powershell','-c',f'(New-Object Media.SoundPlayer "final.wav").PlaySync();'])
    except Exception as e:
        print(f"An error occurred while playing the audio: {e}")

# sample_text = "Hi this is a test input text for AI text generation"
# text_to_speech(sample_text,"gtts_testing.wav")