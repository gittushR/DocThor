#Voicebot UI built using Gradio,could be done using react
import os
import gradio as gr
from doc_analysis import encode_image,analyze_image_with_query
from voice_recorder import voice_recorder, generate_transcription
from doc_output import text_to_speech

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Do not say 'In the image I see' but say something along the lines of 'With what I see', 'I think you have ....' or similar phrases.
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please. """

def process_inputs(Record_your_query,Share_an_image):
    patient_query = generate_transcription(Record_your_query)

    if Share_an_image:
        doctor_response = analyze_image_with_query(system_prompt + patient_query,encode_image(Share_an_image))
    else:
        doctor_response = "No image for me to analyze. Share an image and I may be able to help"

    doctor_voice =  text_to_speech(doctor_response,"final.mp3")
    return patient_query,doctor_response,doctor_voice

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=['microphone'],type='filepath'),
        gr.Image(type='filepath')
    ],
    outputs=[
        gr.Textbox(label='Speech to Text'),
        gr.Textbox(label="Doctor's analysis"),
        gr.Audio('Temp.mp3')
    ],
    title='DocTHOR 🩺 '
)

iface.launch(debug=True)