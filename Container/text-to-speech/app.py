import gradio as gr
from transformers import pipeline
from datasets import load_dataset

import torch
import numpy as np


synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")

def text_to_speech(text, speaker_id):
    speaker_embedding = torch.tensor(embeddings_dataset[int(speaker_id)]["xvector"]).unsqueeze(0)
    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})

    return speech["sampling_rate"], np.array(speech["audio"])


with gr.Blocks(title="Text to Speech") as app:
    gr.Markdown("# Text to Speech")
    with gr.Row():
        text_input = gr.Textbox(label="Enter your text")
        speaker_id_input = gr.Textbox(label="Speaker ID (0-7306)", value="7306")
    
    output_audio = gr.Audio(label="Generated Speech")
    submit_btn = gr.Button("Generate Speech", variant="primary")

    submit_btn.click(
        fn=text_to_speech, 
        inputs=[text_input, speaker_id_input],
        outputs=output_audio
    )


if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
