import os
import time
import torch
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from huggingface_hub import InferenceClient
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorer
from threading import Thread

# Knowledge base context for Neiman Marcus
SYSTEM_PROMPT = """You are the official AI Portfolio Assistant for Neiman Marcus (Engineer Marcus).
Marcus is a Senior Software Engineer specializing in Python, AI Agents, Automation, Linux Dev Environments, and Backend Infrastructure.

Core Facts about Marcus:
- Location: Nairobi, Kenya (open to remote & international roles)
- GitHub: https://github.com/engineermarcus (32+ public repositories)
- Email: engineermarcus72@gmail.com
- Core Stack: Python, TypeScript, JavaScript, Shell, Kotlin, C

Key Repositories:
1. cybernetics & positron: Browser-based Linux shell & IDE via global npm with secure cloud tunneling and AI voice assistant.
2. moviebox-api (Magpie CLI): Headless Playwright media crawler executing inside Termux on Android via proot Ubuntu container with chunked httpx downloads and Internet Archive upload.
3. marcus-enterprises: Reusable Paystack payment gateway on Render powering the AM2PM Liquor Store storefront in Kileleshwa, Nairobi.
4. agents & rag-qa-system: Production autonomous multi-agent pipelines with tool calling and vector retrieval-augmented generation.
5. colibri: Pure C frontier MoE model runner with zero dependencies, streaming active expert weights directly from disk.
6. cuckoo & rodent-app: Native Android mobile apps built with Kotlin and Coroutines.
7. tcp: Tailscale mesh network linking Android phone and development workstation.

GitHub Achievements:
- Quickdraw: Solved and closed issue/PR within 5 minutes.
- Pull Shark: Merged pull requests across repositories.
- YOLO: Merged PRs without review, demonstrating rapid delivery.

Instructions:
Be concise, technical, precise, and enthusiastic about Marcus's work. Answer questions directly using the knowledge above.
"""

HF_TOKEN = os.environ.get("HF_TOKEN", "")
LOCAL_MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

print(f"Loading local model {LOCAL_MODEL_ID} on CPU...")
try:
    tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        LOCAL_MODEL_ID,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )
    model.eval()
    print("Local Qwen2.5 model loaded successfully!")
except Exception as e:
    print(f"Notice: local model load exception ({e}). Will use InferenceClient as primary.")
    model = None
    tokenizer = None

client = InferenceClient(api_key=HF_TOKEN) if HF_TOKEN else None

def generate_answer(query: str, history: list = None) -> str:
    # 1. Try local Qwen model first
    if model is not None and tokenizer is not None:
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            if history:
                for h in history[-3:]:
                    if isinstance(h, (list, tuple)) and len(h) == 2:
                        messages.append({"role": "user", "content": str(h[0])})
                        messages.append({"role": "assistant", "content": str(h[1])})
            messages.append({"role": "user", "content": query})
            
            prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer([prompt_text], return_tensors="pt")
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9
                )
            generated_ids = outputs[:, inputs.input_ids.shape[1]:]
            response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            if response.strip():
                return response.strip()
        except Exception as e:
            print(f"Local generation error: {e}")

    # 2. Try Hugging Face Inference Router with Qwen2.5
    if client:
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ]
            res = client.chat.completions.create(
                model="Qwen/Qwen2.5-Coder-32B-Instruct",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            return res.choices[0].message.content.strip()
        except Exception as e:
            print(f"InferenceClient error: {e}")

    # 3. Fallback knowledge synthesizer
    q = query.lower()
    if "moviebox" in q or "magpie" in q or "termux" in q:
        return "moviebox-api (Magpie CLI) is a headless media-fetch CLI running inside Termux on Android via a proot Ubuntu container. It drives Playwright Chromium to score sources and streams video chunks down via httpx with live progress and Internet Archive synchronization."
    elif "paystack" in q or "store" in q or "client" in q:
        return "Marcus Enterprises is a reusable Express payment gateway on Render wrapping Paystack. It powers AM2PM Liquor Store (Kileleshwa, Nairobi) with automated order sessions and cryptographic HMAC webhook verification."
    elif "colibri" in q or "c" in q or "moe" in q:
        return "Colibri is a pure C inference runner for frontier Mixture-of-Experts models. Built with zero dependencies, it streams expert weights dynamically from disk to execute models on hardware with limited VRAM."
    elif "achievement" in q or "badge" in q:
        return "Marcus holds 3 GitHub achievements: Quickdraw (closed issue/PR within 5 min), Pull Shark (merged PRs across repositories), and YOLO (merged PRs without review)."
    else:
        return f"Marcus is a senior software engineer with 32+ public repositories specializing in Python, AI agents, cloud dev environments (cybernetics & positron), and systems infrastructure."

# FastAPI REST Application
fastapi_app = FastAPI(title="Neiman Marcus AI Agent API")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@fastapi_app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "engine": "Qwen2.5",
        "has_local_model": model is not None,
        "repos": 32,
        "achievements": ["Quickdraw", "Pull Shark", "YOLO"]
    }

@fastapi_app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    last_query = req.messages[-1].content if req.messages else "Hello"
    reply = generate_answer(last_query)
    return {
        "response": reply,
        "model": "Qwen2.5-Instruct",
        "timestamp": time.time()
    }

# Gradio Interface
def gradio_chat(message, history):
    return generate_answer(message, history)

demo = gr.ChatInterface(
    fn=gradio_chat,
    title="Neiman Marcus — AI Agent & Automation Engine",
    description="Interactive Qwen2.5 AI agent answering technical queries about Marcus's 32+ repositories, Termux headless pipelines, and systems architecture.",
    examples=[
        "What are Marcus's core AI and automation projects?",
        "Explain how moviebox-api runs Playwright inside Termux Android",
        "Tell me about the Paystack Payment Gateway and client storefront",
        "What is Colibri and how does it run MoE models in pure C?",
        "What GitHub achievements does Marcus hold?"
    ]
)

# Mount Gradio onto FastAPI
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
