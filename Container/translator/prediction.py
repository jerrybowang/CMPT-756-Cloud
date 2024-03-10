import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM

# 指向你克隆的仓库中模型所在的本地目录
# change to opus-mt-zh-en for testing, /app/ is only for docker directory
local_model_directory = "/app/opus-mt-zh-en"

model = TFAutoModelForSeq2SeqLM.from_pretrained(local_model_directory)
tokenizer = AutoTokenizer.from_pretrained(local_model_directory)

def translation_eng(text: str) -> str:
    # Assuming 'tokenizer' and 'model' are already initialized and suitable for translation

    input_ids = tokenizer.encode(text, return_tensors="tf")
    output = model.generate(input_ids)
    decoded_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return decoded_text