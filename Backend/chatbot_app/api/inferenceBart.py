# Old inference code is belows code.
import torch, time
from transformers import BartTokenizer, BartForConditionalGeneration
import os
 
# Load the tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-base')

# Define the checkpoint path
checkpoint_path = os.path.join(os.getcwd(),"final_checkpoint.pth")
 
# Function to load checkpoint
def load_checkpoint(model, file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Checkpoint file not found at: {file_path}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(file_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    print("Checkpoint loaded successfully.")

load_checkpoint(model, checkpoint_path)
model.eval()

# Function to generate answers
def ask_question(question, object_name=None, max_length=50):
    if model is None:
        raise RuntimeError("Model is not loaded. Ensure the checkpoint is available.")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    #START MEASURING TIME
    start_time = time.time()

    # Prepare the input
    combined_input = f"{object_name} {question}" if object_name else question
    inputs = tokenizer(
        combined_input,
        return_tensors="pt",
        max_length=128,
        truncation=True
    ).to(device)

    generation_start_time = time.time()

    # Generate answer
    answer_ids = model.generate(
        inputs['input_ids'],
        max_length=max_length,
        num_beams=4,
        early_stopping=True
    )


    generation_time = time.time() - generation_start_time
    print(f"Generation Time: {generation_time:.4f} seconds")

    total_time = time.time() - start_time
    print(f"Total Time (for question generation): {total_time:.4f} seconds")

    answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)
    return answer



