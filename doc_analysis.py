#This script will generate a response by analysing the input image and the text provided by the patient.
#The patient voice will be recorded in voice_recorder and converted to text in doc output script
#and will be sent here for analysis and the output
#generated here will be translated to doctors speech in doc output script
import os
import base64
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

#image_path = "acne.jpg"
def encode_image(image_path):
    image_file = open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_query(query,encoded_image,model=None):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }
        ],
        model=model or "meta-llama/llama-4-scout-17b-16e-instruct",
    )
    return chat_completion.choices[0].message.content