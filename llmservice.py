import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from logger import logger
import asyncio
import os

# Point to the local folder so it loads instantly
MODEL_PATH = "./local_model" 

logger.info("Loading model from local storage...")

if torch.cuda.is_available():
    MODEL_DEVICE = "cuda"
    MODEL_DTYPE = torch.float16
else:
    MODEL_DEVICE = "cpu"
    MODEL_DTYPE = torch.float32

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=MODEL_DTYPE,
    local_files_only=True
).to(MODEL_DEVICE)

model.eval()
logger.info(f"Model loaded on {MODEL_DEVICE}")

def generate_reply_sync(prompt: str):
    # Llama 3.2 uses different tags, let's use the tokenizer's built-in tool
    inputs = tokenizer(prompt, return_tensors="pt").to(MODEL_DEVICE)
    
    with torch.inference_mode(): # Faster than no_grad()
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,      # Small models need a little "creative" room to not loop
            temperature=0.1,     # But keep it low for accuracy
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )

    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Logic to extract only the answer part
    if "assistant" in full_text.lower():
        answer = full_text.split("assistant")[-1].strip()
    else:
        answer = full_text.replace(prompt, "").strip()
        
    return answer

async def generate_reply(prompt: str):
    return await asyncio.to_thread(generate_reply_sync, prompt)