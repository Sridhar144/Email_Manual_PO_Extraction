from transformers import pipeline, logging

def setup_llama():
    logging.set_verbosity_error()
    text_gen_model = pipeline(
        "text-generation",
        model="meta-llama/Llama-3.2-3B-Instruct",
        torch_dtype="bfloat16",
        device_map="auto",
    )
    classifier_model = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",
    )
    return text_gen_model, classifier_model
