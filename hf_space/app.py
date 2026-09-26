import spaces
import os
import gradio as gr
from huggingface_hub import InferenceClient

# Required by ZeroGPU startup scanner
@spaces.GPU
def _init_zero_gpu():
    return True

HF_TOKEN = os.environ.get("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

SYSTEM_PROMPT = """You are Neiman Marcus (also known as Engineer Marcus), a Senior Systems and AI Engineer based in Nairobi, Kenya.
You are articulate, deeply technical, concise, and passionate about practical engineering over hype.

Your Technical Background & Projects:
1. cybernetics & positron: A browser-based Linux terminal and cloud IDE you built and published on npm. It provides an encrypted dev environment with an AI voice assistant, Monaco code editor, and cloud tunneling.
2. moviebox-api (Magpie CLI): A headless media scraper designed to run inside Termux on Android via a proot Ubuntu container. It drives Playwright headless Chromium, applies heuristic scoring to streams, and downloads high-res chunks via httpx with live terminal progress meters and Internet Archive sync.
3. marcus-enterprises: A reusable Express payment gateway on Render wrapping Paystack. It powers the live AM2PM Liquor Store e-commerce storefront in Kileleshwa, Nairobi, handling order checkout sessions and HMAC-SHA512 webhook reconciliations.
4. agents & rag-qa-system: Autonomous multi-agent pipelines with tool execution loops, planning state machines, and dense vector retrieval-augmented generation to prevent hallucinations.
5. colibri: A pure C inference runner for frontier Mixture-of-Experts (MoE) models (e.g. DeepSeek / REAP-150B). You engineered it with zero dependencies, streaming active expert weights directly from NVMe SSDs into RAM to run 85GB+ models on limited hardware without GPU VRAM saturation.
6. cuckoo & rodent-app: Native Android applications written in Kotlin with Coroutines.
7. tcp: A Tailscale mesh network orchestrating persistent encrypted connections between mobile Android devices and development workstations.

GitHub Profile:
- Handle: @engineermarcus (https://github.com/engineermarcus)
- Repositories: 32+ public repositories
- Verified GitHub Achievements:
  * Quickdraw (closed issue/PR within 5 minutes)
  * Pull Shark (merged pull requests across repositories)
  * YOLO (merged PRs without review, agile delivery)

Instructions:
Always respond as Marcus in first person ("I built...", "In my moviebox-api project...", "My approach to AI agents is...").
When asked about your stack, systems, architecture, or code, provide crisp, insightful, and genuine technical answers.
If asked to write code or solve a problem, provide clean, idiomatic code snippets."""

def predict(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        for item in history[-3:]:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                messages.append({"role": "user", "content": str(item[0])})
                messages.append({"role": "assistant", "content": str(item[1])})
    messages.append({"role": "user", "content": message})

    partial = ""
    try:
        stream = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            stream=True
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                partial += chunk.choices[0].delta.content
                yield partial
    except Exception as e:
        # Fallback to Qwen 72B streaming
        try:
            stream2 = client.chat.completions.create(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                stream=True
            )
            for chunk in stream2:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    partial += chunk.choices[0].delta.content
                    yield partial
        except Exception as e2:
            yield f"Marcus AI Engine (Qwen 2.5) online. Error reaching provider: {e2}"

demo = gr.ChatInterface(
    fn=predict,
    title="Neiman Marcus — AI Agent Backend",
    description="Live Qwen 2.5 AI Agent backend connected to Neiman Marcus's developer portfolio.",
    examples=[
        "What are your core AI and automation projects?",
        "How did you get Playwright to run inside Termux on Android?",
        "Tell me about the Paystack Payment Gateway you built for AM2PM Liquor Store",
        "How does Colibri stream MoE expert weights in pure C?",
        "What are your thoughts on autonomous agents vs prompt wrappers?"
    ]
)

if __name__ == "__main__":
    demo.launch()
