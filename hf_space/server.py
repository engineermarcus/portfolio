"""
Neiman Marcus Portfolio - AI Agent Backend
FastAPI server powered by Qwen 2.5 models and Hugging Face Inference API.
Provides interactive conversational endpoints, project querying, and agent workflow simulation.
"""

import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient

app = FastAPI(
    title="Neiman Marcus - Portfolio AI Agent API",
    description="Interactive backend supporting Marcus's portfolio, agent workflow simulations, and Qwen2.5 LLM completions.",
    version="1.0.0"
)

# Enable CORS for GitHub Pages, local development, and Hugging Face spaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
PRIMARY_MODEL = os.environ.get("HF_MODEL", "Qwen/Qwen2.5-Coder-32B-Instruct")

# Portfolio knowledge context injected into every prompt
PORTFOLIO_CONTEXT = """
You are the official AI Assistant for Neiman Marcus (Engineer Marcus), an experienced Software Engineer specializing in Python, AI Agents, Automation, Backend Infrastructure, and Developer Tooling.

Key Details about Marcus:
- Location: Nairobi, Kenya (open to remote & global contracts).
- Primary Stack: Python, TypeScript, JavaScript, Shell, Kotlin, C.
- GitHub: https://github.com/engineermarcus (32+ public repositories).
- Email: engineermarcus72@gmail.com
- GitHub Achievements:
  * Quickdraw (closed issue/PR within 5 minutes)
  * Pull Shark (multiple merged PRs across repositories)
  * YOLO (merged PRs without review, agile & confident shipping)

Key Projects:
1. Cybernetics & Positron: Browser-based Linux shell and IDE deployable globally via npm with tunneled HTTPS, AI voice assistant, and cloud terminal.
2. Moviebox-API (Magpie): Headless media-fetch CLI running inside Termux on Android via proot Ubuntu container using Playwright, httpx chunk streaming, and Internet Archive synchronization.
3. Marcus Enterprises & AM2PM Liquor Store: Reusable Node/Express Paystack payment gateway deployed on Render powering an e-commerce storefront in Kileleshwa, Nairobi.
4. AI Agents & RAG-QA-System: Autonomous multi-agent pipelines, tool use, prompt chaining, and retrieval-augmented generation.
5. Colibri: Pure C frontier MoE model runner with zero dependencies, streaming experts from disk.
6. Cuckoo & Rodent-App: Native Android mobile apps written in Kotlin.
7. TCP: Tailscale mesh network orchestrating phone and dev machine connectivity.
8. Cyberlink: npm package for multi-source search aggregation with AI summarization layer.

Instructions for your responses:
- Always represent Marcus accurately, professionally, and enthusiastically.
- Provide crisp, technical, informative answers.
- Highlight his hands-on experience in full-stack architecture, agentic automation, and systems engineering.
- When asked for code or architecture, provide clean, idiomatic snippets.
"""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512

class ChatResponse(BaseModel):
    response: str
    model: str
    status: str = "ok"

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Neiman Marcus Portfolio Agent Backend",
        "model": PRIMARY_MODEL,
        "docs": "/docs",
        "endpoints": ["/api/chat", "/api/projects", "/api/status"]
    }

@app.get("/api/status")
def get_status():
    return {
        "status": "healthy",
        "model": PRIMARY_MODEL,
        "has_token": bool(HF_TOKEN),
        "version": "1.0.0",
        "achievements": ["Quickdraw", "Pull Shark", "YOLO"],
        "repo_count": 32
    }

@app.get("/api/projects")
def get_projects():
    # Return structured portfolio data
    return {
        "profile": {
            "name": "Neiman Marcus",
            "title": "Software Engineer — AI & Systems",
            "github": "https://github.com/engineermarcus",
            "bio": "Software engineer with a focus on Python, AI agents, and automation tooling."
        },
        "categories": [
            "AI & Autonomous Agents",
            "Developer Infrastructure & Cloud Shells",
            "Headless Automation & Media Pipelines",
            "Production & Client Products",
            "Open Source & Curricula"
        ]
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat_completion(req: ChatRequest):
    selected_model = req.model or PRIMARY_MODEL
    
    # Try calling Hugging Face InferenceClient
    if HF_TOKEN:
        try:
            client = InferenceClient(api_key=HF_TOKEN)
            
            # Format messages with system context
            formatted_messages = [{"role": "system", "content": PORTFOLIO_CONTEXT}]
            for msg in req.messages:
                formatted_messages.append({"role": msg.role, "content": msg.content})
                
            res = client.chat.completions.create(
                model=selected_model,
                messages=formatted_messages,
                max_tokens=req.max_tokens or 512,
                temperature=req.temperature or 0.7
            )
            reply = res.choices[0].message.content
            return ChatResponse(response=reply, model=selected_model)
        except Exception as e:
            print(f"HF Inference error ({e}), falling back to intelligent knowledge engine.")
            
    # Fallback knowledge synthesis engine
    last_user_msg = req.messages[-1].content.lower() if req.messages else ""
    
    if "project" in last_user_msg or "what have you built" in last_user_msg:
        reply = (
            "Marcus has built an extensive catalog of 32+ public projects! Key highlights include:\n"
            "- **Cybernetics & Positron**: Browser-based Linux shell & IDE with AI voice assistant.\n"
            "- **Moviebox-API (Magpie)**: Headless Playwright media CLI running inside Termux on Android.\n"
            "- **Marcus Enterprises**: Paystack payment gateway powering live retail (AM2PM Liquor Store).\n"
            "- **AI Agents & RAG-QA**: Production multi-agent pipelines and vector Q&A systems.\n"
            "- **Colibri**: Pure C frontier MoE model runner streaming experts from disk."
        )
    elif "ai" in last_user_msg or "agent" in last_user_msg:
        reply = (
            "Marcus specializes in agentic AI and workflow automation:\n"
            "1. Multi-agent coordination with tool calling, planning, and self-correction.\n"
            "2. Local LLM optimization (running small models like Qwen2.5 1B-7B and frontier MoE in pure C).\n"
            "3. RAG pipelines combining vector search, chunking, and document QA.\n"
            "4. Multimodal real-time voice and vision integration with Gemini Live."
        )
    elif "contact" in last_user_msg or "hire" in last_user_msg or "email" in last_user_msg:
        reply = "You can contact Marcus directly at **engineermarcus72@gmail.com** or connect on GitHub at [github.com/engineermarcus](https://github.com/engineermarcus). He is available for senior engineering roles, AI agent architecture, and consulting."
    elif "achievement" in last_user_msg or "badge" in last_user_msg:
        reply = "Marcus holds 3 official GitHub Achievements:\n- 🎯 **Quickdraw**: Solved & closed an issue/PR within 5 minutes.\n- 🦈 **Pull Shark**: Merged pull requests across repositories.\n- ⚡ **YOLO**: Merged PRs rapidly without code review."
    else:
        reply = (
            f"Hello! I'm Marcus's AI portfolio agent. I can guide you through his 32+ repositories, "
            f"AI agent architectures, headless automation pipelines, or full-stack production deployments. "
            f"What would you like to explore?"
        )
        
    return ChatResponse(response=reply, model="qwen-portfolio-engine (local)")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
